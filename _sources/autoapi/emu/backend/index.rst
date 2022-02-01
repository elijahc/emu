:py:mod:`emu.backend`
=====================

.. py:module:: emu.backend


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   emu.backend.list
   emu.backend.add_collaborator
   emu.backend.get_file_manifest



Attributes
~~~~~~~~~~

.. autoapisummary::

   emu.backend.folder_app


.. py:data:: folder_app
   

   

.. py:function:: list(id = typer.Argument(...))


.. py:function:: add_collaborator(id = typer.Argument(...), role = CollaborationRole.EDITOR, collaborator = typer.Argument(..., help='collaborator to add. May be a User, Group, or email address (unicode string)'), notify = False, can_view_path = False)


.. py:function:: get_file_manifest(folder, prog_bar=False, **kwargs)


