# Architecture Decision Records

The intention is to document deviations from a standard Model View Controller (MVC) design.

AP Mapper follows the standard Nautobot app architecture with no significant deviations:

- **Models**: `APFloorPlan` and `ObjectPlacement` use standard Django ORM with GenericForeignKey for flexible object placement
- **Views**: Standard Django class-based views and Nautobot UI ViewSets
- **Templates**: Standard Django templates extending Nautobot generic templates
- **API**: Standard Nautobot REST API viewsets and serializers
