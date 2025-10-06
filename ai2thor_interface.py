import ai2thor.controller
import matplotlib.pyplot as plt

controller = ai2thor.controller.Controller(scene="FloorPlan1")

def execute_action(action_json):
    if action_json is None:
        print("Invalid command")
        return
    action = action_json.get("action")
    if action == "MoveAhead":
        steps = action_json.get("steps", 1)
        for _ in range(steps):
            controller.step(action="MoveAhead")
    elif action == "RotateRight":
        rotation = action_json.get("rotation", 90)
        controller.step(action="RotateRight", degrees=rotation)
    elif action == "PickupObject":
        obj = action_json.get("object")
        if obj:
            controller.step(action="PickupObject", objectId=obj)
    # Show frame
    event = controller.step(action="Pass")
    plt.imshow(event.frame)
    plt.axis('off')
    plt.show()
