from django import forms
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

from .search_filter import SearchFilter


class SearchForm(forms.Form):
    search = forms.CharField(
        label=_('search'),
        max_length=100,
        required=False)


class SeliaList(object):
    paginate_by = 5
    prefix = ''

    def get_context_data(self, request):
        return {
            'templates': self.get_templates(),
            'queryset': self.get_queryset(request),
            'forms': self.get_forms()
        }


    def get_templates(self):
        return {
            'list_item': self.get_list_item_template(),
            'filter_form': self.get_filter_form_template(),
        }

    def get_forms(self):
        forms = {}

        if hasattr(self, 'filter'):
            forms['filter'] = self.filter

        if hasattr(self, 'search_form'):
            forms['search'] = self.search_form

        if hasattr(self, 'order_form'):
            forms['order'] = self.order_form

        return forms

    def get_ordering_choices(self):
        orderings = []
        for field, label in self.ordering_fields:
            orderings.append(
                (
                    '-{field}'.format(field=field),
                    '{order} {label}'.format(
                        label=label, order=_('↓'))
                )
            )

            orderings.append(
                (
                    field,
                    '{order} {label}'.format(
                        label=label, order=_('↑'))
                    )
                )
        return orderings

    def get_ordering_form_class(self):
        ordering_choices = self.get_ordering_choices()

        class OrderingForm(forms.Form):
            order = forms.ChoiceField(
                label=_('ordering'),
                choices=ordering_choices)

        return OrderingForm

    def get_ordering_form(self, request):
        ordering_form_class = self.get_ordering_form_class()
        ordering_form_prefix = self.get_ordering_form_prefix()

        ordering_form = ordering_form_class(
            request.GET,
            prefix=ordering_form_prefix)

        return ordering_form

    def get_search_form(self, request):
        search_form_prefix = self.get_search_form_prefix()
        return SearchForm(request.GET, prefix=search_form_prefix)

    def get_ordering_form_prefix(self):
        return '{}_order'.format(self.prefix)

    def get_search_form_prefix(self):
        return '{}_search'.format(self.prefix)

    def get_filter_form_prefix(self):
        return '{}_filter'.format(self.prefix)

    def get_filter_form_template(self):
        if hasattr(self, 'filter_form_template'):
            return self.filter_form_template

        return NotImplementedError('No template for filter form was given')

    def get_filter_class(self):
        if hasattr(self, 'filter_class'):
            return self.filter_class

        raise NotImplementedError('No filter class was provided')

    def get_initial_queryset(self):
        if hasattr(self, 'queryset'):
            return self.queryset

        raise NotImplementedError('No initial queryset was provided')

    def paginate_queryset(self, queryset, request):
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page', 1)
        page = paginator.get_page(page)
        return page

    def get_queryset(self, request):
        queryset = self.get_initial_queryset()
        filtered_queryset = self.filter_queryset(queryset, request)
        return self.paginate_queryset(filtered_queryset, request)

    def filter_queryset_with_query(self, queryset, request):
        try:
            filter_class = self.get_filter_class()
            prefix = self.get_filter_form_prefix()
            self.filter = filter_class(
                request.GET,
                request=request,
                queryset=queryset,
                prefix=prefix)
            queryset = self.filter.qs
        except NotImplementedError:
            pass

        return queryset

    def filter_queryset_with_search(self, queryset, request):
        if hasattr(self, 'search_fields'):
            self.search_form = self.get_search_form(request)

            if self.search_form.is_valid():
                queryset = SearchFilter().filter_queryset(request, queryset, self)

        return queryset

    def order_queryset(self, queryset, request):
        if hasattr(self, 'ordering_fields'):
            self.order_form = self.get_ordering_form(request)

            if self.order_form.is_valid():
                ordering_form_prefix = self.get_ordering_form_prefix()
                query_param = '{}-order'.format(ordering_form_prefix)
                ordering = self.order_form.data[query_param]
                queryset = queryset.order_by(ordering)

        return queryset

    def filter_queryset(self, queryset, request):
        queryset = self.filter_queryset_with_query(queryset, request)
        queryset = self.filter_queryset_with_search(queryset, request)
        queryset = self.order_queryset(queryset, request)
        return queryset

    def get_list_item_template(self):
        if hasattr(self, 'list_item_template'):
            return self.list_item_template

        return NotImplementedError('No template for list item was given')
