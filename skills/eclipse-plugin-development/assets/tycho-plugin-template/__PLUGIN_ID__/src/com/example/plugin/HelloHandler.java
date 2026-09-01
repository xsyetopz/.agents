package __JAVA_PACKAGE__;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.ui.handlers.HandlerUtil;

public final class HelloHandler extends AbstractHandler {
    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        MessageDialog.openInformation(
                HandlerUtil.getActiveShellChecked(event),
                "__PLUGIN_NAME__",
                "Hello from __PLUGIN_NAME__");
        return null;
    }
}
