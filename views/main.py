import Main_View from Main_View
import model.Main_Model
  
# Initialize MVC components
    model = Main_Model()
    view = Main_View(None)  # Controller will be set in next line
    controller = Main_Controller(model, view)
    
    # Build the application
    controller.build(page)