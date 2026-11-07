import enum
import subprocess


@enum.unique
class UrgencyLevel(str, enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    CRITICAL = "critical"


def send_message(body: str, expire_time: int = 10):
    urgency: UrgencyLevel = UrgencyLevel.NORMAL
    # icon = dir + "icon.png"
    title = "forty"
    body = body.replace("-", "\-")
    arguments = ['notify-send']
    arguments.append(title)
    arguments.append(body)
    arguments.append(f"--expire-time={expire_time * 1000}")
    arguments.append(f"--urgency={urgency}")
    # arguments.append(f"--icon={icon}")
    arguments.append("--hint=int:transient:1")
    # arguments.append("--app-name=forty")
    subprocess.Popen(arguments)


__all__ = ["send_message"]
