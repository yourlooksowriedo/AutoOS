"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const path = require("path");
const sudo = require('sudo-prompt');
const REG_JUMP_BIN = `${path.resolve(__dirname, '../bin/regjump.exe')} "{key}"`;
const sudoOptions = {
    name: 'RegJump'
};
function activate(context) {
    context.subscriptions.push(vscode.commands.registerTextEditorCommand('extension.reg.jumpToKey', jumpToRegKey));
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
function jumpToRegKey(textEditor, edit) {
    textEditor.selections.forEach(function (selection) {
        var document = textEditor.document;
        var line = document.lineAt(selection.anchor);
        var text = textEditor.document.getText(line.range);
        var regMatches = text.match(/\[(.*?)\]/);
        if (regMatches) {
            var command = REG_JUMP_BIN.replace("{key}", regMatches[1]);
            sudo.exec(command, sudoOptions, function (err, stdout, stderr) {
                if (err) {
                    console.log(err);
                    vscode.window.showErrorMessage(`RegJump faild, ${err}`);
                    return;
                }
            });
        }
    });
}
//# sourceMappingURL=extension.js.map