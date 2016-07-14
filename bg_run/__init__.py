
def load_ipython_extension(shell):
    from .magics import AsyncMagics
    shell.register_magics(AsyncMagics)

def unload_ipython_extension(shell):
    from .magics import AsyncMagics
    shell.magics_manager.registry['AsyncMagics'].pool.shutdown()
    for magic_type,magics in AsyncMagics.magics.items():
        for magic in magics:
            del shell.magics_manager.magics[magic_type][magic]
    del shell.magics_manager.registry['AsyncMagics']

