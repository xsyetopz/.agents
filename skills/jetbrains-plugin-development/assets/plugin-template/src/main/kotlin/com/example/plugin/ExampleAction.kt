package __PACKAGE__

import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.project.DumbAware
import com.intellij.openapi.ui.Messages

class ExampleAction : AnAction(), DumbAware {
    override fun actionPerformed(event: AnActionEvent) {
        Messages.showInfoMessage(
            event.project,
            PluginBundle.message("action.example.message"),
            PluginBundle.message("action.example.message"),
        )
    }
}
