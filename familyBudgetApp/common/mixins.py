class RefererURLMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['referer_url'] = self.request.META.get('HTTP_REFERER')
        return context


class SearchMixin:
    def get_search_term(self):
        search_term = self.request.GET.get("name", None)
        print("Search term:", search_term)  # Add this line for debugging
        return search_term

    def apply_search_filter(self, queryset):
        search_term = self.get_search_term()

        if search_term:
            queryset = queryset.filter(name__icontains=search_term)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.apply_search_filter(queryset)


class CategoryFilterMixin:
    def get_search_category(self):
        category = self.request.GET.get("category", None)
        print("Category:", category)  # Add this line for debugging
        return category

    def apply_category_filter(self, queryset):
        category = self.get_search_category()

        if category:
            queryset = queryset.filter(item_type=category)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.apply_category_filter(queryset)


class TagFilterMixin:
    def get_search_tag_id(self):
        return self.request.GET.get("tag", None)

    def apply_tag_filter(self, queryset):
        search_tag_id = self.get_search_tag_id()

        if search_tag_id:
            queryset = queryset.filter(tags__id=search_tag_id)

        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.apply_tag_filter(queryset)  # Apply tag filter
        return queryset