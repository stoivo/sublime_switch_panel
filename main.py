import sublime
from sublime_plugin import WindowCommand


class Mixin():
    def output_panels(self):
        return [p for p in self.window.panels() if self.include_panel(p)]

    def include_panel(self, name):
        return name != "output.find_results" and \
               name.startswith("output")


class PsOutputPanelCommand(Mixin, WindowCommand):
    def run(self, idx=0):
        self.panels = self.output_panels()
        if len(self.panels) == 0:
            self.window.status_message("No panels found")
            return
        self.window.show_quick_panel(
            self.explucive_panel_names(self.panels),
            self.on_select,
            idx,
            0,
            self.on_hightlight)

    def explucive_panel_names(self, panels):
        def name(panel):
            name = panel[len("output."):]
            view = self.window.find_output_panel(name)
            if view.file_name() is None or view.name() == "":
                return name
            else:
                return [name, "{} {}".format(view.file_name() or "", view.name())]

        return [name(p) for p in panels]

    def on_select(self, idx):
        if idx == -1:
            return

        self.window.run_command("show_panel", {"panel": self.panels[idx]})

    def on_hightlight(self, idx):
        if idx == -1:
            return

        if self.window.active_panel() != self.panels[idx]:
            self.window.run_command("show_panel", {"panel": self.panels[idx]})


class PsOutputPanelNextCommand(Mixin, WindowCommand):
    def run(self):
        panels = self.output_panels()
        try:
            idx = panels.index(self.window.active_panel())
            next_idx = (idx+1) % len(panels)
            self.window.run_command("show_panel", {"panel": panels[next_idx]})
        except ValueError as e:
            self.window.run_command("show_panel", {"panel": panels[0]})
