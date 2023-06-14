import asyncio
from typing import Callable
from jupytercad import CadDocument
from y_py import YMapEvent


class JcadNotification:
    def __init__(self, doc: CadDocument) -> None:
        self._jcad_doc = doc
        self._highlighted_shape = {}
        self._callback = None
        yobjects = self._jcad_doc.ydoc.get_array("objects")
        yobjects.observe_deep(self._on_change)
        doc.ydoc.observe_after_transaction(self.after_transaction)
        self.target_name = None

    def connect(self, f: Callable):
        self._callback = f

    def disconnect(self):
        self._callback = None

    def _on_change(self, events):
        for event in events:
            if not isinstance(event, YMapEvent):
                continue
            if "shapeMetadata" not in event.keys:
                self.target_name = event.target["name"]


    def after_transaction(self, e):
        if self._callback is not None and self.target_name is not None:
            target_name = self.target_name
            self.target_name = None
            passed, msg = self._callback()
            if not passed:
                asyncio.create_task(self._add_warning(target_name, msg))
            else:
                asyncio.create_task(self._remove_warning())
            

    async def _remove_warning(self):
        for old_name, old_annotation_id in self._highlighted_shape.items():
            self._jcad_doc.set_color(old_name, None)
            self._jcad_doc.remove_annotation(old_annotation_id)
        self._highlighted_shape = {}

    async def _add_warning(self, name, message):
        for old_name, old_annotation_id in self._highlighted_shape.items():
            if old_name != name:
                self._jcad_doc.set_color(old_name, None)
            self._jcad_doc.remove_annotation(old_annotation_id)
            
        self._jcad_doc.set_color(name, [1, 0, 0])
        annotation_id = self._jcad_doc.add_annotation(
            name,
            message,
            user={"color": "#0000ff30", "initials": "BO", "display_name": "Bot"},
        )
        self._highlighted_shape = {name: annotation_id}
