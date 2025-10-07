from django.views.decorators.cache import cache_page

__all__ = ['BaseDispatchCache']


class BaseDispatchCache:
    cache_timeout = None

    def dispatch(self, *args, **kwargs):
        if self.cache_timeout is not None:
            original_dispatch = super().dispatch
            decorated_dispatch = cache_page(self.cache_timeout)(original_dispatch)
            return decorated_dispatch(*args, **kwargs)
        else:
            return super().dispatch(*args, **kwargs)
