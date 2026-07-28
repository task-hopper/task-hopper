from dataclasses import dataclass, field


@dataclass
class Registry:
    _commands: dict[str, str] = field(default_factory=dict)

    def register(self, command_name: str, carrot_name: str) -> None:
        """Register a command name as owned by a carrot. Raises on collision."""
        if command_name in self._commands:
            owner = self._commands[command_name]
            raise ValueError(
                f"Command '{command_name}' is already registered by carrot '{owner}'. "
                f"Carrot '{carrot_name}' cannot be installed without conflict."
            )
        self._commands[command_name] = carrot_name

    def owner(self, command_name: str) -> str | None:
        return self._commands.get(command_name)

    def all_commands(self) -> dict[str, str]:
        return dict(self._commands)


registry = Registry()
