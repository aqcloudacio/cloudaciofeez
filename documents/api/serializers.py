from rest_framework import serializers

from documents.models import Theme, Style, Structure, Element, Content
from users.models import Practice, AFSL

#####


class ThemeSerializer(serializers.ModelSerializer):

    active_practices = serializers.PrimaryKeyRelatedField(queryset=Practice.objects.all(),
                                                          many=True,
                                                          allow_null=True,
                                                          required=False)
    styles = serializers.SerializerMethodField()
    afsls = serializers.PrimaryKeyRelatedField(queryset=AFSL.objects.all(),
                                                many=True,
                                                allow_null=True,
                                                required=False)

    def get_styles(self, instance):
        # for some reason the styles PK related field was bugging out DRF,
        # and not correctly linking a default style to a newly created theme.
        # so have changed to a method field
        if instance.styles.exists():
            return [instance.styles.all()[0].id]



    class Meta:
        model = Theme
        fields = "__all__"


class StyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Style
        fields = "__all__"


class StructureSerializer(serializers.ModelSerializer):

    general_full_width_subheader1 = serializers.ReadOnlyField()
    general_full_width_subheader2 = serializers.ReadOnlyField()

    fee_display_alternative_platform = serializers.ReadOnlyField()
    fee_split_platform_types = serializers.ReadOnlyField()
    fee_portrait_overflow_limit = serializers.ReadOnlyField()
    fee_landscape_overflow_limit = serializers.ReadOnlyField()
    fee_change_orientation_if_overflow = serializers.ReadOnlyField()
    fee_display_percentage_subtotal = serializers.ReadOnlyField()
    fee_display_percentage_total = serializers.ReadOnlyField()
    fee_display_NA_flat_fees = serializers.ReadOnlyField()
    fee_display_null_rows = serializers.ReadOnlyField()
    fee_percentage_position = serializers.ReadOnlyField()

    aa_hide_variance = serializers.ReadOnlyField()
    aa_hide_risk_profile = serializers.ReadOnlyField()
    aa_hide_bar_chart = serializers.ReadOnlyField()
    aa_include_cur_vs_rp = serializers.ReadOnlyField()
    aa_include_rec_vs_rp = serializers.ReadOnlyField()
    aa_include_cur_vs_rp_vs_rec = serializers.ReadOnlyField()
    aa_include_cur_vs_rec = serializers.ReadOnlyField()

    product_hide_percentage = serializers.ReadOnlyField()
    product_hide_ICR = serializers.ReadOnlyField()

    class Meta:
        model = Structure
        fields = "__all__"


class ElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Element
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    content_type_list = serializers.SerializerMethodField()
    element_name = serializers.SerializerMethodField()


    class Meta:
        model = Content
        fields = "__all__"

    def get_content_type_list(self, obj):
        return obj.TABLE_TYPE_CHOICES

    def get_element_name(self,obj):
        return str(obj.element)
