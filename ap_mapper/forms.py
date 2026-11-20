"""Forms for ap_mapper."""

from django import forms
from nautobot.apps.forms import (
    ContentTypeModelMultipleChoiceField,
    DynamicModelChoiceField,
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
    TagFilter,
    TagsBulkEditFormMixin,
)
from nautobot.dcim.models import Location

from ap_mapper import models


class APFloorPlanForm(NautobotModelForm):
    """APFloorPlan creation/edit form."""

    location = DynamicModelChoiceField(
        queryset=Location.objects.all(),
        help_text="The Location that owns this floor plan.",
    )

    class Meta:
        model = models.APFloorPlan
        fields = [
            "location",
            "name",
            "description",
            "logical_width",
            "logical_height",
            "background",
            "tags",
        ]
        widgets = {
            "background": forms.ClearableFileInput(attrs={"accept": "image/png,image/jpeg,image/svg+xml"}),
        }


class APFloorPlanBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):
    """APFloorPlan bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.APFloorPlan.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False, max_length=255)
    name = forms.CharField(required=False, max_length=255)

    class Meta:
        nullable_fields = ["description", "name"]


class APFloorPlanFilterForm(NautobotFilterForm):
    """Filter form for APFloorPlan."""

    model = models.APFloorPlan
    field_order = ["q", "location", "name"]

    q = forms.CharField(required=False, label="Search", help_text="Search within Name.")
    location = DynamicModelChoiceField(queryset=Location.objects.all(), required=False, label="Location")
    name = forms.CharField(required=False, label="Name")


class ObjectPlacementForm(NautobotModelForm):
    """ObjectPlacement creation/edit form."""

    floor_plan = DynamicModelChoiceField(
        queryset=models.APFloorPlan.objects.all(),
        required=True,
        help_text="The floor plan map this placement belongs to.",
    )
    object_type = forms.ChoiceField(
        choices=[
            ("wireless.wirelessap", "Wireless AP"),
            ("dcim.device", "Device"),
            ("dcim.rack", "Rack"),
            ("dcim.location", "Location"),
        ],
        label="Object Type",
        help_text="Type of object to place on the map.",
    )

    class Meta:
        model = models.ObjectPlacement
        fields = ["floor_plan", "object_type", "object_id", "x", "y", "color", "label", "tags"]
        widgets = {
            "object_id": forms.HiddenInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        object_type = cleaned_data.get("object_type")
        object_id = cleaned_data.get("object_id")
        if object_type and object_id:
            try:
                from django.contrib.contenttypes.models import ContentType

                ct = ContentType.objects.get(app_label=object_type.split(".")[0], model=object_type.split(".")[1])
                cleaned_data["content_type"] = ct
            except ContentType.DoesNotExist:
                self.add_error("object_type", "Invalid object type.")
        return cleaned_data


class ObjectPlacementBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):
    """ObjectPlacement bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ObjectPlacement.objects.all(), widget=forms.MultipleHiddenInput
    )
    color = forms.CharField(required=False, max_length=7)
    label = forms.CharField(required=False, max_length=255)

    class Meta:
        nullable_fields = ["color", "label"]


class ObjectPlacementFilterForm(NautobotFilterForm):
    """Filter form for ObjectPlacement."""

    model = models.ObjectPlacement
    field_order = ["q", "floor_plan", "object_type"]

    q = forms.CharField(required=False, label="Search")
    floor_plan = DynamicModelChoiceField(queryset=models.APFloorPlan.objects.all(), required=False)
    object_type = ContentTypeModelMultipleChoiceField(
        queryset=None,
        required=False,
        label="Object Type",
    )


class PlacementPickerForm(forms.Form):
    """Form used in the map editor to pick an object to place."""

    target = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Type to search..."}),
        help_text="Search for objects to place on the map.",
    )
