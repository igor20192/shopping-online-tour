from oscar.apps.catalogue.views import ProductCategoryView as CoreProductCategoryView
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from bs4 import BeautifulSoup
from oscar.apps.catalogue.models import ProductCategory, Product
from django.shortcuts import get_list_or_404


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
        context["keywords"] = self.get_meta_keywords()
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name
        )
        context.update(search_context)
        return context

    def get_meta_keywords(self):
        """
        Returns a comma-separated list of product names associated with the category, for use in the keywords meta tags.
        """
        product_id = ProductCategory.objects.filter(
            category_id=self.kwargs["pk"]
        ).values("product_id")
        index_list = [index["product_id"] for index in product_id]
        return ",".join(
            values["title"]
            for values in Product.objects.filter(id__in=index_list).values("title")
        )


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
        ctx["keywords"] = self.object.title
        return ctx
