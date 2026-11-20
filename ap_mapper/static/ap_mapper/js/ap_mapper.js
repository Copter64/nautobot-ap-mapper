/**
 * AP Mapper - Interactive Leaflet map with object markers
 */
(function() {
    'use strict';

    let map = null;
    let markersLayer = null;
    let backgroundLayer = null;
    let isEditMode = false;
    let pendingPlacements = []; // [{id, object_id, object_name, object_url, object_type, x, y, color, is_new}]
    let originalRevision = 0;
    let selectedObject = null; // {id, name, url, type} from picker

    // DOM references
    const loadingEl = document.getElementById('apm-loading');
    const errorEl = document.getElementById('apm-error');
    const noMapEl = document.getElementById('apm-no-map');
    const mapContainer = document.getElementById('apm-map-container');

    // Load data from JSON script tags
    function getJson(id) {
        const el = document.getElementById(id);
        return el ? JSON.parse(el.textContent) : null;
    }

    const floorPlanId = getJson('apm-floorplan-id');
    const mapWidth = getJson('apm-map-width') || 1000;
    const mapHeight = getJson('apm-map-height') || 1000;
    const backgroundUrl = getJson('apm-background-url') || '';
    const initialPlacements = getJson('apm-placements') || [];
    const editPermission = getJson('apm-edit-permission') || false;
    const apiPlacementsUrl = getJson('apm-api-placements-url') || '';
    const csrfToken = getJson('apm-csrf-token') || '';
    const supportedTypes = getJson('apm-supported-types') || [];

    /**
     * Initialize the Leaflet map
     */
    function initMap() {
        if (!mapContainer) return;

        mapContainer.classList.remove('apm-hidden');
        loadingEl.classList.add('apm-hidden');

        // Simple CRS for a fixed-size image (no projection)
        const bounds = [[0, 0], [mapHeight, mapWidth]];

        map = L.map('apm-map-container', {
            crs: L.CRS.Simple,
            bounds: bounds,
            minZoom: -2,
            maxZoom: 6,
            zoomControl: true,
            attributionControl: false,
        });

        // Background image layer
        if (backgroundUrl) {
            backgroundLayer = L.imageOverlay(backgroundUrl, bounds).addTo(map);
        } else {
            // Fallback: blank canvas with grid
            backgroundLayer = L.rectangle(bounds, {
                color: '#ccc',
                weight: 1,
                fillColor: '#f8f9fa',
                fillOpacity: 0.5,
            }).addTo(map);
        }

        map.fitBounds(bounds);

        // Markers layer
        markersLayer = L.layerGroup().addTo(map);

        // Load initial placements
        initialPlacements.forEach(function(p) {
            addMarker(p);
        });

        // Map click handler (for placing objects in edit mode)
        map.on('click', function(e) {
            if (isEditMode && selectedObject) {
                const placement = {
                    id: null,
                    object_id: selectedObject.id,
                    object_name: selectedObject.name,
                    object_url: selectedObject.url,
                    object_type: selectedObject.type,
                    x: Math.round(e.latlng.lng),
                    y: Math.round(e.latlng.lat),
                    color: '#0d6efd',
                    is_new: true,
                };
                pendingPlacements.push(placement);
                addMarker(placement);
                selectedObject = null;
                document.getElementById('apm-picker-place').disabled = true;
            }
        });
    }

    /**
     * Add a marker to the map
     */
    function addMarker(placement) {
        const icon = L.divIcon({
            className: 'apm-marker',
            html: `<div class="apm-marker-dot" style="background-color:${placement.color || '#0d6efd'}"></div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12],
        });

        const marker = L.marker([placement.y, placement.x], {
            icon: icon,
            draggable: isEditMode,
        });

        // Tooltip with object name
        marker.bindTooltip(placement.object_name || 'Unnamed', {
            permanent: false,
            direction: 'top',
            className: 'apm-marker-tooltip',
        });

        // Popup with details and link
        const popupContent = `
            <strong>${placement.object_name || 'Unnamed'}</strong><br>
            Type: ${placement.object_type}<br>
            Position: (${placement.x}, ${placement.y})
            ${placement.object_url ? `<br><a href="${placement.object_url}">View in Nautobot</a>` : ''}
        `;
        marker.bindPopup(popupContent);

        // Drag end handler (update position)
        if (isEditMode) {
            marker.on('dragend', function(e) {
                const latlng = e.target.getLatLng();
                const newX = Math.round(latlng.lng);
                const newY = Math.round(latlng.lat);
                placement.x = newX;
                placement.y = newY;
                marker.setTooltipContent(`${placement.object_name || 'Unnamed'} (${newX}, ${newY})`);
            });

            // Double-click to delete in edit mode
            marker.on('dblclick', function() {
                if (confirm(`Delete placement for "${placement.object_name}"?`)) {
                    markersLayer.removeLayer(marker);
                    const idx = pendingPlacements.findIndex(p => p.id === placement.id);
                    if (idx > -1) {
                        if (!placement.is_new) {
                            placement.is_deleted = true;
                        } else {
                            pendingPlacements.splice(idx, 1);
                        }
                    }
                }
            });
        }

        // Click to select (link to object)
        marker.on('click', function(e) {
            if (!isEditMode && placement.object_url) {
                window.open(placement.object_url, '_blank');
            }
            L.DomEvent.stopPropagation(e);
        });

        marker._placementData = placement;
        markersLayer.addLayer(marker);
    }

    /**
     * Toggle edit mode
     */
    function toggleEditMode(enable) {
        isEditMode = enable;
        const editBtn = document.getElementById('btn-apm-edit');
        const addBtn = document.getElementById('btn-apm-add-object');
        const saveBtn = document.getElementById('btn-apm-save');
        const cancelBtn = document.getElementById('btn-apm-cancel');

        if (enable) {
            editBtn.style.display = 'none';
            if (addBtn) addBtn.style.display = '';
            if (saveBtn) saveBtn.style.display = '';
            if (cancelBtn) cancelBtn.style.display = '';

            // Make existing markers draggable
            markersLayer.eachLayer(function(marker) {
                marker.dragging.enable();
            });
        } else {
            editBtn.style.display = '';
            if (addBtn) addBtn.style.display = 'none';
            if (saveBtn) saveBtn.style.display = 'none';
            if (cancelBtn) cancelBtn.style.display = 'none';

            markersLayer.eachLayer(function(marker) {
                marker.dragging.disable();
            });
        }
    }

    /**
     * Save placements to the API
     */
    async function savePlacements() {
        const saveBtn = document.getElementById('apm-save');
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="mdi mdi-loading mdi-spin"></i> Saving...';

        try {
            // Process new placements
            for (const p of pendingPlacements) {
                if (p.is_new) {
                    await apiPost(apiPlacementsUrl, {
                        floor_plan: floorPlanId,
                        content_type: p.object_type,
                        object_id: p.object_id,
                        x: p.x,
                        y: p.y,
                        color: p.color,
                    });
                } else if (!p.is_deleted) {
                    // Check if position changed
                    const original = initialPlacements.find(ip => ip.id === p.id);
                    if (original && (original.x !== p.x || original.y !== p.y || original.color !== p.color)) {
                        await apiPatch(`${apiPlacementsUrl}${p.id}/`, {
                            x: p.x,
                            y: p.y,
                            color: p.color,
                        });
                    }
                }
            }

            // Delete removed placements
            for (const p of pendingPlacements) {
                if (p.is_deleted) {
                    await apiDelete(`${apiPlacementsUrl}${p.id}/`);
                }
            }

            // Success — reload the map
            alert('Map saved successfully!');
            window.location.reload();
        } catch (err) {
            if (err.status === 409) {
                document.getElementById('apm-conflict-modal').classList.add('show');
                document.getElementById('apm-conflict-modal').style.display = 'block';
            } else {
                showError('Failed to save: ' + err.message);
            }
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="mdi mdi-content-save"></i> Save';
        }
    }

    /**
     * Cancel edits
     */
    function cancelEdits() {
        pendingPlacements = [];
        toggleEditMode(false);
        // Reload markers from initial state
        markersLayer.clearLayers();
        initialPlacements.forEach(function(p) {
            addMarker(p);
        });
    }

    /**
     * Show error
     */
    function showError(message) {
        errorEl.classList.remove('apm-hidden');
        document.getElementById('apm-error-message').textContent = message;
        mapContainer.classList.add('apm-hidden');
    }

    /**
     * API helpers
     */
    async function apiRequest(url, method, data) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
        };
        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        if (!response.ok) {
            const err = await response.json().catch(() => ({detail: response.statusText}));
            throw new Error(err.detail || err.message || response.statusText);
        }
        return response.json();
    }

    function apiPost(url, data) { return apiRequest(url, 'POST', data); }
    function apiPatch(url, data) { return apiRequest(url, 'PATCH', data); }
    function apiDelete(url) { return apiRequest(url, 'DELETE'); }

    // Object picker
    function initPicker() {
        const searchInput = document.getElementById('apm-object-search');
        const typeSelect = document.getElementById('apm-object-type');
        const resultsEl = document.getElementById('apm-picker-results');
        const placeBtn = document.getElementById('apm-picker-place');

        let debounceTimer = null;

        async function searchObjects() {
            const query = searchInput.value.trim();
            const type = typeSelect.value;

            if (query.length < 2) {
                resultsEl.innerHTML = '<p class="text-muted small">Type at least 2 characters...</p>';
                return;
            }

            resultsEl.innerHTML = '<p class="text-muted small">Searching...</p>';

            try {
                // Use the Nautobot API search endpoint
                const [appLabel, modelName] = type.split('.');
                const apiUrl = `/api/${appLabel}/${modelName.replace(/_/g, '-')}/?limit=10&q=${encodeURIComponent(query)}`;

                const response = await fetch(apiUrl, {
                    headers: { 'X-CSRFToken': csrfToken },
                });
                const data = await response.json();

                if (data.results.length === 0) {
                    resultsEl.innerHTML = '<p class="text-muted small">No results found.</p>';
                    return;
                }

                resultsEl.innerHTML = data.results.map(r => `
                    <div class="apm-picker-result" data-id="${r.id}" data-name="${r.display || r.name}"
                         data-url="${r.url}" data-type="${type}" style="cursor:pointer; padding:6px; border-bottom:1px solid #eee;">
                        ${r.display || r.name}
                    </div>
                `).join('');

                // Click to select
                resultsEl.querySelectorAll('.apm-picker-result').forEach(el => {
                    el.addEventListener('click', function() {
                        resultsEl.querySelectorAll('.apm-picker-result').forEach(e => e.style.background = '');
                        el.style.background = '#e7f1ff';
                        selectedObject = {
                            id: this.dataset.id,
                            name: this.dataset.name,
                            url: this.dataset.url,
                            type: this.dataset.type,
                        };
                        placeBtn.disabled = false;
                    });
                });
            } catch (err) {
                resultsEl.innerHTML = `<p class="text-danger small">Search failed: ${err.message}</p>`;
            }
        }

        searchInput.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(searchObjects, 300);
        });

        typeSelect.addEventListener('change', searchObjects);

        placeBtn.addEventListener('click', function() {
            if (!selectedObject) return;
            // Close modal, user clicks on map to place
            document.getElementById('apm-picker-modal').classList.remove('show');
            document.getElementById('apm-picker-modal').style.display = 'none';
            alert(`Click on the map to place "${selectedObject.name}"`);
        });
    }

    // Event bindings
    document.addEventListener('DOMContentLoaded', function() {
        if (!floorPlanId) {
            noMapEl.classList.remove('apm-hidden');
            loadingEl.classList.add('apm-hidden');
            return;
        }

        initMap();
        initPicker();

        const editBtn = document.getElementById('btn-apm-edit');
        if (editBtn && editPermission) {
            editBtn.addEventListener('click', function() { toggleEditMode(true); });
        }

        const addBtn = document.getElementById('btn-apm-add-object');
        if (addBtn) {
            addBtn.addEventListener('click', function() {
                document.getElementById('apm-picker-modal').classList.add('show');
                document.getElementById('apm-picker-modal').style.display = 'block';
            });
        }

        const saveBtn = document.getElementById('btn-apm-save');
        if (saveBtn) {
            saveBtn.addEventListener('click', savePlacements);
        }

        const cancelBtn = document.getElementById('btn-apm-cancel');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', cancelEdits);
        }

        const reloadBtn = document.getElementById('btn-apm-reload');
        if (reloadBtn) {
            reloadBtn.addEventListener('click', function() { window.location.reload(); });
        }

        const conflictReload = document.getElementById('apm-conflict-reload');
        if (conflictReload) {
            conflictReload.addEventListener('click', function() { window.location.reload(); });
        }
    });
})();
