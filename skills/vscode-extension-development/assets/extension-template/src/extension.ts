import * as vscode from "vscode";
import { greeting } from "./core.ts";

export function activate(context: vscode.ExtensionContext): void {
  context.subscriptions.push(
    vscode.commands.registerCommand("__EXTENSION_NAME__.hello", () => {
      void vscode.window.showInformationMessage(greeting("workspace"));
    }),
  );
}

export function deactivate(): void {}
