from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

__all__ = ["BaseDispatchCache"]


class BaseDispatchCache:
    cache_timeout = None

    def dispatch(self, *args, **kwargs):
        if self.cache_timeout is not None:
            original_dispatch = super().dispatch
            decorated_dispatch = vary_on_cookie(
                cache_page(self.cache_timeout)(original_dispatch)
            )
            return decorated_dispatch(*args, **kwargs)
        else:
            return super().dispatch(*args, **kwargs)
