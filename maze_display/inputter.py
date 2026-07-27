from __future__ import annotations
from typing import TYPE_CHECKING
import a_maze_ing
import config
import random
from maze_display.structures import MenuState, Color

if TYPE_CHECKING:
    from maze_display.renderer import Renderer


class Inputter():
    def __init__(self, context: Renderer):
        self.ctx: Renderer = context

        self.feedback_msg: str = ""
        self.is_quitting: bool = False
        self.menu_state: MenuState = MenuState.main
        self.tile_target: str = ""

    def main_menu(self) -> None:
        """Displays main menu.

        Display options include:
            Re-generating a new maze,
            Show / Hide the shortest path,
            Customize maze,
            Quit
        """
        if self.is_quitting:
            return
        print("=== A-Maze-ing ===")
        print(f"{Color.LES}1. Re-generate a new maze{Color.END}")
        print(f"{Color.LES}2. Show / Hide the shortest path{Color.END}")
        print(f"{Color.LES}3. Customize maze colors{Color.END}")
        print(f"{Color.LES}4. Adjust animation speed{Color.END}")
        print(f"{Color.LES}5. Quit{Color.END}")
        while 1:
            try:
                choice = input(f"{Color.SRT}Choice? (1-5): {Color.END}")
            except (KeyboardInterrupt, EOFError):
                self.feedback_msg = (
                    f"{Color.ERR}Keyboard interrupt, "
                    f"aborting.{Color.END}"
                )
                self.ctx.inputter.is_quitting = True
                self.ctx.pipeline.display(False)
                return
            match choice:
                case "1":
                    seed: int = random.randint(-999999, 999999)
                    self.feedback_msg = (f"{Color.SCS}Generating new maze "
                                         f"(SEED: {seed}){Color.END}")
                    self.ctx.pipeline.is_anim = True
                    self.menu_state = MenuState.main
                    c: config.Config | None
                    c, self.ctx.ani = a_maze_ing.generate_output(seed)
                    if not c or not self.ctx.ani:
                        return
                    assert c._output_file is not None
                    self.ctx.output_name = c._output_file
                    try:
                        self.ctx.read_output()
                    except (FileNotFoundError, PermissionError,
                            IsADirectoryError):
                        print(f"{Color.ERR}Data not found, "
                              f"aborting.{Color.END}")
                        return
                    self.ctx.main_render()
                    break
                case "2":
                    if self.ctx.is_show_path:
                        self.feedback_msg = (f"{Color.SCS}Toggling to hide "
                                             f"shortest path...{Color.END}")
                    else:
                        self.feedback_msg = (f"{Color.SCS}Toggling to show "
                                             f"shortest path...{Color.END}")
                    self.ctx.pipeline.is_anim = False
                    self.ctx.is_show_path = not self.ctx.is_show_path
                    self.menu_state = MenuState.main
                    self.ctx.pipeline.maze_render()
                    self.ctx.pipeline.display(False)
                    break
                case "3":
                    self.feedback_msg = (f"{Color.SCS}Setting color "
                                         f"of...{Color.END}")
                    self.ctx.pipeline.is_anim = False
                    self.menu_state = MenuState.tile
                    self.ctx.pipeline.display(False)
                    break
                case "4":
                    self.feedback_msg = (f"{Color.SCS}Listening to new "
                                         "animation speed... "
                                         f"(default: 0.01){Color.END}")
                    self.ctx.pipeline.is_anim = False
                    self.menu_state = MenuState.respeed
                    self.ctx.pipeline.display(False)
                    break
                case "5":
                    self.feedback_msg = (f"{Color.SCS}Quitting "
                                         f"process...{Color.END}")
                    self.ctx.pipeline.is_anim = False
                    self.is_quitting = True
                    self.ctx.pipeline.display(False)
                    break
                case _:
                    self.feedback_msg = (f"{Color.ERR}Unrecognized input. "
                                         f"Try again.{Color.END}")
                    self.ctx.pipeline.is_anim = False
                    self.menu_state = MenuState.main
                    self.ctx.pipeline.display(False)
                    break

    def tile_menu(self) -> None:
        """Displays the type type menu when re-coloring.

        Display options include:
            Background Color,
            Border Color,
            Wall Color,
            Path Color,
            Start Color,
            Exit Color,
            Logo Color,
            Go Back
        """
        print("=== A-Maze-ing ===")
        print(f"{Color.LES}1. Background Color{Color.END}")
        print(f"{Color.LES}2. Border Color{Color.END}")
        print(f"{Color.LES}3. Wall Color{Color.END}")
        print(f"{Color.LES}4. Path Color{Color.END}")
        print(f"{Color.LES}5. Start Color{Color.END}")
        print(f"{Color.LES}6. Exit Color{Color.END}")
        print(f"{Color.LES}7. Logo Color{Color.END}")
        print(f"{Color.LES}8. Go Back{Color.END}")

        try:
            choice = input(f"{Color.SRT}Choice? (1-8): {Color.END}")
        except (KeyboardInterrupt, EOFError):
            self.feedback_msg = (
                f"{Color.ERR}Keyboard interrupt, "
                f"aborting.{Color.END}"
            )
            self.ctx.inputter.is_quitting = True
            self.menu_state = MenuState.main
            self.ctx.pipeline.display(False)
            return
        match choice:
            case "1":
                self.tile_target = "background"
            case "2":
                self.tile_target = "border"
            case "3":
                self.tile_target = "wall"
            case "4":
                self.tile_target = "path"
            case "5":
                self.tile_target = "start"
            case "6":
                self.tile_target = "exit"
            case "7":
                self.tile_target = "logo"
            case "8":
                self.feedback_msg = ("")
                self.menu_state = MenuState.main
                self.ctx.pipeline.display(False)
                return
            case _:
                self.feedback_msg = (f"{Color.ERR}Unrecognized input. "
                                     f"Try again.{Color.END}")
                self.ctx.pipeline.display(False)
                return

        self.feedback_msg = (f"{Color.SCS}Setting the color of "
                             f"{self.tile_target.capitalize()} "
                             f"to...{Color.END}")
        self.menu_state = MenuState.color
        self.ctx.pipeline.display(False)

    def color_menu(self) -> None:
        """Displays color menu.

        This only shows up once a tile type has been specified.

        Display options include:
            All supported colors,
            Go Back
        """
        print("=== A-Maze-ing ===")
        print(f"{Color.black}██{Color.END} {Color.LES}1. Black{Color.END}")
        print(f"{Color.red}██{Color.END} {Color.LES}2. Red{Color.END}")
        print(f"{Color.green}██{Color.END} {Color.LES}3. Green{Color.END}")
        print(f"{Color.yellow}██{Color.END} {Color.LES}4. Yellow{Color.END}")
        print(f"{Color.blue}██{Color.END} {Color.LES}5. Blue{Color.END}")
        print(f"{Color.magenta}██{Color.END} {Color.LES}6. Magenta{Color.END}")
        print(f"{Color.cyan}██{Color.END} {Color.LES}7. Cyan{Color.END}")
        print(f"{Color.white}██{Color.END} {Color.LES}8. White{Color.END}")
        print(f"{Color.bright_black}██{Color.END} "
              f"{Color.LES}9. Bright Black{Color.END}")
        print(f"{Color.bright_red}██{Color.END} "
              f"{Color.LES}10. Bright Red{Color.END}")
        print(f"{Color.bright_green}██{Color.END} "
              f"{Color.LES}11. Bright Green{Color.END}")
        print(f"{Color.bright_yellow}██{Color.END} "
              f"{Color.LES}12. Bright Yellow{Color.END}")
        print(f"{Color.bright_blue}██{Color.END} "
              f"{Color.LES}13. Bright Blue{Color.END}")
        print(f"{Color.bright_magenta}██{Color.END} "
              f"{Color.LES}14. Bright Magenta{Color.END}")
        print(f"{Color.bright_cyan}██{Color.END} "
              f"{Color.LES}15. Bright Cyan{Color.END}")
        print(f"{Color.bright_white}██{Color.END} "
              f"{Color.LES}16. Bright White{Color.END}")
        print(f"{Color.LES}17. Go Back{Color.END}")

        chosen_color: str = ""
        try:
            choice = input(f"{Color.SRT}Choice? (1-17): {Color.END}")
        except (KeyboardInterrupt, EOFError):
            self.feedback_msg = (
                f"{Color.ERR}Keyboard interrupt, "
                f"aborting.{Color.END}"
            )
            self.ctx.inputter.is_quitting = True
            self.menu_state = MenuState.main
            self.ctx.pipeline.display(False)
            return

        match choice:
            case "1":
                chosen_color = "black"
            case "2":
                chosen_color = "red"
            case "3":
                chosen_color = "green"
            case "4":
                chosen_color = "yellow"
            case "5":
                chosen_color = "blue"
            case "6":
                chosen_color = "magenta"
            case "7":
                chosen_color = "cyan"
            case "8":
                chosen_color = "white"
            case "9":
                chosen_color = "bright_black"
            case "10":
                chosen_color = "bright_red"
            case "11":
                chosen_color = "bright_green"
            case "12":
                chosen_color = "bright_yellow"
            case "13":
                chosen_color = "bright_blue"
            case "14":
                chosen_color = "bright_magenta"
            case "15":
                chosen_color = "bright_cyan"
            case "16":
                chosen_color = "bright_white"
            case "17":
                self.feedback_msg = ("")
                self.menu_state = MenuState.main
                self.ctx.pipeline.display(False)
                return
            case _:
                self.feedback_msg = (f"{Color.ERR}Unrecognized input. "
                                     f"Try again.{Color.END}")
                self.ctx.pipeline.display(False)
                return

        self.feedback_msg = (f"{Color.SCS}Setting "
                             f"{self.tile_target.capitalize()} to "
                             f"{chosen_color}...{Color.END}")
        self.ctx.color[self.tile_target] = getattr(Color, chosen_color)
        self.ctx.pipeline.is_anim = False
        self.menu_state = MenuState.main
        self.ctx.pipeline.maze_render()
        self.ctx.pipeline.display(False)

    def respeed_menu(self) -> None:
        """Displays animation speed adjust menu."""
        print("=== A-Maze-ing ===")
        try:
            choice = input(f"{Color.SRT}New speed? ('q' to quit): {Color.END}")
        except (KeyboardInterrupt, EOFError):
            self.feedback_msg = (
                f"{Color.ERR}Keyboard interrupt, "
                f"aborting.{Color.END}"
            )
            self.ctx.inputter.is_quitting = True
            self.menu_state = MenuState.main
            self.ctx.pipeline.display(False)
            return

        if choice.lower() == "q":
            self.feedback_msg = ""
            self.menu_state = MenuState.main
            self.ctx.pipeline.display(False)
            return

        try:
            self.ctx.pipeline.anim_speed = min(float(choice), 10.0)
        except ValueError:
            self.feedback_msg = (f"{Color.ERR}Not a float. "
                                 f"Try again.{Color.END}")
            self.ctx.pipeline.display(False)
            return
        if self.ctx.pipeline.anim_speed <= 0:
            self.feedback_msg = (f"{Color.SCS}Disabling animation..."
                                 f"{Color.END}")
        else:
            self.feedback_msg = (f"{Color.SCS}Setting animation speed to "
                                 f"{self.ctx.pipeline.anim_speed}..."
                                 f"{Color.END}")
        self.menu_state = MenuState.main
        self.ctx.pipeline.maze_render()
        self.ctx.pipeline.display(False)

    def wait_menu(self, dot_count: int) -> None:
        """Displays a waiting string instead of a menu.

        Args:
            dot_count (int): Amount of dots after message (0-3)
        """
        print("=== A-Maze-ing ===")
        dot_str: str = ""
        for dot in range(dot_count):
            dot_str += "."
        print(
            f"{Color.LES}Currently generating, "
            f"please wait{dot_str}{Color.END}"
        )
