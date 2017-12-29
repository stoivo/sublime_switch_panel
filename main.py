import sublime
from sublime_plugin import WindowCommand


class PsOutputPanelCommand(WindowCommand):
    def run(self, idx=0):
        self.panels = [p for p in self.window.panels() if self.include_panel(p)]
        if len(self.panels) == 0:
            self.window.status_message("No panels found")
            return
        self.window.show_quick_panel(self.panels, self.on_select, idx, 0, self.on_hightlight)

    def on_select(self, idx):
        if idx == -1:
            return

        self.window.run_command("show_panel", {"panel": self.panels[idx]})

    def on_hightlight(self, idx):
        if idx == -1:
            return

        if self.window.active_panel() != self.panels[idx]:
            self.window.run_command("show_panel", {"panel": self.panels[idx]})

    def include_panel(self, name):
        return name != "output.find_results" and \
               name.startswith("output")
