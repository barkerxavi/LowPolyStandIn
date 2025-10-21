import maya.cmds as cmds
import maya.utils
import maya.OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtWidgets

WINDOW_TITLE = "My PySide6 Dock"
WORKSPACE_CONTROL_NAME = "MyPySide6DockWorkspaceControl"


def get_maya_main_window():
    """Return Maya's main window as a QtWidget."""
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), QtWidgets.QMainWindow)
    return None


def dock_window():
    """Create the dock and defer the actual widget embedding until Maya's UI is ready."""
    # Delete any existing dock
    if cmds.workspaceControl(WORKSPACE_CONTROL_NAME, exists=True):
        cmds.deleteUI(WORKSPACE_CONTROL_NAME)

    # Create the workspace control container
    cmds.workspaceControl(
        WORKSPACE_CONTROL_NAME,
        label=WINDOW_TITLE,
        retain=False
    )

    # Make it visible immediately
    cmds.workspaceControl(WORKSPACE_CONTROL_NAME, e=True, visible=True)
    cmds.workspaceControl(WORKSPACE_CONTROL_NAME, e=True, restore=True)

    # Defer UI building until Maya finishes constructing the control
    maya.utils.executeDeferred(_finish_docking)


def _finish_docking():
    """Attach our PySide6 widget to the workspaceControl."""
    workspace_ptr = omui.MQtUtil.findControl(WORKSPACE_CONTROL_NAME)
    if not workspace_ptr:
        cmds.warning(f"Could not find workspace control '{WORKSPACE_CONTROL_NAME}'")
        return

    workspace_qt = wrapInstance(int(workspace_ptr), QtWidgets.QWidget)

    # Create our custom widget
    main_window = get_maya_main_window()
    my_widget = MyDockableWindow(parent=main_window)

    # Clear existing layout (Maya sometimes pre-populates it)
    if workspace_qt.layout():
        old_layout = workspace_qt.layout()
        QtWidgets.QWidget().setLayout(old_layout)

    # Add the custom widget
    layout = QtWidgets.QVBoxLayout(workspace_qt)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(my_widget)
    layout.update()

    my_widget.show()
    workspace_qt.update()
    cmds.refresh(force=True)

    print(f"{WORKSPACE_CONTROL_NAME} dock successfully created!")



# Example usage:
# dock_window()
