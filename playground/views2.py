from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):
    # for assign tags to a given object we first need object_id for content_type,
    # then go to taggeditem model we have to pre load the tagfield and applied a filter
    content_type = ContentType.objects.get_for_model(Product)
    queryset = TaggedItem.objects\
        .select_related('tag')\
        .filter(content_type=content_type,object_id=1)

    context = {
        'name':'Paras',
        'result':list(queryset)
    }
    return render(request, 'hello.html', context)
