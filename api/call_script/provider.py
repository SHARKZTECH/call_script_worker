from injector import Module, provider, singleton
from api.call_script.service import CallScriptService


class CallScriptModule(Module):
    @singleton
    @provider
    def provide_synthesizer(self) -> CallScriptService:
        return CallScriptService()
