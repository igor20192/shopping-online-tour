from oscar.apps.catalogue.views import ProductCategoryView as CoreProductCategoryView
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from bs4 import BeautifulSoup


class ProductCategoryView(CoreProductCategoryView):
    """
    View to display the product category page.

    Inherits from CoreProductCategoryView and adds additional context information for display.

    Methods:
    - get_context_data(self, **kwargs): Returns context data for the template, including category information, description, keywords, and search data.
    - get_meta_keywords(self): Returns a comma-separated list of product names associated with the category, for use in the keywords meta tags.
    """

    def get_context_data(self, **kwargs):
        """
        Returns context data for the template, including category information, description, keywords, and search data.
        """
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["description"] = BeautifulSoup(
            context["category"].description, "html.parser"
        ).text.strip()
        context["keywords"] = self.category.keywords
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name
        )
        context.update(search_context)
        return context


class ProductDetailView(CoreProductDetailView):
    """
    View to display the product detail page.

    Inherits from CoreProductDetailView and adds additional context information for display, related to alerts and keywords.

    Methods:
    - get_context_data(self, **kwargs): Returns context data for the template, including the alert form, alert status, and product name as keywords.
    """

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["alert_form"] = self.get_alert_form()
        ctx["has_active_alert"] = self.get_alert_status()
        ctx["keywords"] = self.object.keywords
        return ctx
