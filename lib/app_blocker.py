class IPBlocker:
    def block(self, ip: str) -> bool:
        raise NotImplementedError()

    def unblock(self, ip: str) -> bool:
        raise NotImplementedError()
