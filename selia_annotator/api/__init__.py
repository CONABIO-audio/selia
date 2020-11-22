"""
API Module for Selia Annotator App.


This module builds API REST endpoints to provide required information
needed to build the Annotation App. The exposed actions are:

1) Get information on an Item. In particular the url for item download,
the list of admissible events for annotation, the adequate visualizer for its
item type and relevant metadata.
2) Get the list of Annotations associated to an Item. The list is filtered
according to the user permissions.
3) Create/Update/Delete a annotation. These actions are only allowed if the user
role permits it.
4) Get information on the current collection to consult admissible annotation
and event types.
5) Get user permission information.
6) Retrieve all annotation votes.
7) Create/Update/Delete annotations votes.
8) Get the list of all model predictions of the current Item.
9) Create/Update/Delete model predictions votes.

"""
