use zed_extension_api as zed;

struct ExampleExtension;

impl zed::Extension for ExampleExtension {
    fn new() -> Self {
        Self
    }

    fn language_server_command(
        &mut self,
        _language_server_id: &zed::LanguageServerId,
        worktree: &zed::Worktree,
    ) -> zed::Result<zed::Command> {
        let command = worktree.which("__SERVER_BINARY__").ok_or_else(|| {
            "Install __SERVER_BINARY__ or configure a managed download".to_owned()
        })?;

        Ok(zed::Command {
            command,
            args: Vec::new(),
            env: worktree.shell_env(),
        })
    }
}

zed::register_extension!(ExampleExtension);
