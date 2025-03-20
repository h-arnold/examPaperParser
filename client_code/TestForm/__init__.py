from ._anvil_designer import TestFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class TestForm(TestFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def testOcrProcessingButton_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.server.call('main')

  def testListFiles_click(self, **event_args):
    """This method is called when the component is clicked."""
    anvil.server.call('list_files_in_directory')
