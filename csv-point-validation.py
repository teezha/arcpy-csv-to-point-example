import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    self.params[0].value = "H:\\var\\gist\\8138\\mod03\\particulate_data.csv"
    self.params[1].value = "H:\\var\\gist\\8138\\mod03\\gvrdlatlong.shp"
    self.params[2].value = str(self.params[1].value).replace('.','')[:-3] +"_"+ str(self.params[0].value).replace('.','')[-3:]
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    if self.params[0].altered:
      self.params[2].value = str(self.params[1].value).replace('.','')[:-3] +"_"+ str(self.params[0].value).replace('.','')[-3:]
    if self.params[1].altered:
      self.params[2].value = str(self.params[1].value).replace('.','')[:-3] +"_"+ str(self.params[0].value).replace('.','')[-3:]
    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return
