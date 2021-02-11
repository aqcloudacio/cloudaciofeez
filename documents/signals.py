from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, get_list_or_404

from scenarios.models import Report
from documents.models import Style, Theme, Structure, Element, Content

from documents.builder.core import build_document


@receiver(pre_save, sender=Report)
def generate_document(sender, instance, *args, **kwargs):
    '''
    Generates the scenario's document output as a separate model.
    '''
    if not instance.id and not instance.file:

        file = build_document(instance.scenario)

        if file:
            instance.file = file
        else:
            error = {'message': "The document could not be generated."}
            raise Exception(error)



@receiver(post_save, sender=Theme)
def post_save_master(sender, instance, *args, **kwargs):
    create_default_style(sender, instance, *args, **kwargs)
    create_default_structure(sender, instance, *args, **kwargs)
    create_default_content(sender, instance, *args, **kwargs)


def create_default_style(sender, instance, *args, **kwargs):
    '''
    Creates a default Style for a newly created theme
    '''

    if not instance.styles.exists():
        style = Style(theme=instance)
        style.save()
        create_default_elements(sender, instance, args, kwargs)


def create_default_content(sender, instance, *args, **kwargs):
    '''
    Creates all content items for a new theme
    '''
    if not instance.content.exists():
        fee_content_types = (Content.FEE_CHOICES)
        aa_content_types = (Content.AA_CHOICES)
        product_content_types = (Content.PRODUCT_CHOICES)

        table_types = (Content.TABLE_TYPE_CHOICES)

        # Iterate table types
        for table_type in [t[0] for t in table_types]:

            # Select the aplicatable content types for each table and create
            # all of them.
            if table_type == "Product":
                for idx, type in enumerate([t[0] for t in product_content_types]):
                    create_content_item(type, table_type, instance, idx)

            if table_type == "Actual" or table_type == "Consolidated":
                for idx, type in enumerate([t[0] for t in fee_content_types]):
                    create_content_item(type, table_type, instance, idx)

            if table_type == "AA":
                for idx, type in enumerate([t[0] for t in aa_content_types]):
                    create_content_item(type, table_type, instance, idx)


def create_content_item(type, table_type, instance, idx):
    '''
    Creates a custom content item
    '''
    content = Content(theme=instance,
                      type=type,
                      table_type=table_type,
                      order=idx)
    content.save()


def create_default_structure(sender, instance, *args, **kwargs):
    '''
    Creates a default Structure for a newly created theme
    '''
    if not instance.structures.exists():
        structure = Structure(theme=instance)
        structure.save()

def create_default_elements(sender, instance, *args, **kwargs):
    '''
    Creates default Elements for a newly created Theme's default Style
    '''
    style = instance.styles.all()[0]

    if not style.elements.exists():
        element_types = (Element.ELEMENT_TYPE_CHOICES)

        for type in [t[0] for t in element_types]:
            element = Element(style=style,
                              type=type)
            element.save()
