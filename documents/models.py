from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# User = get_user_model()
# Create your models here.


class Theme(models.Model):
    '''
    The settings for the actual document being created.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="themes",
                             blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    template = models.BooleanField(default=False)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.name


class Style(models.Model):
    '''
    The overarching style for the doc/table.
    ONE STYLE PER THEME ONLY
    '''
    theme = models.ForeignKey(Theme,
                             on_delete=models.CASCADE,
                             related_name="styles",
                             blank=True, null=True)

    ### Font options
    font_bold = models.BooleanField(default=False)
    font_color = models.CharField(max_length=20, default="000000")#HEX, no hash
    font_italic = models.BooleanField(default=False)
    font_name = models.CharField(max_length=50, default="Calibri")
    font_size = models.PositiveIntegerField(default=11) #EMUs. 12700EMUs to the pt
    font_small_caps = models.BooleanField(default=False)
    font_underline = models.BooleanField(default=False)

    # Table border options
    border_color = models.CharField(max_length=50, default="000000")
    border_width = models.PositiveSmallIntegerField(default=1)
    border_sides = models.CharField(max_length=50,
                                    default="top,bottom,insideV,insideH",
                                    null=True) #e.g. "top,bottom,start,end,insideH,insideV"

    # Table cell margin options
    cell_margin_top = models.DecimalField(default=56.693, max_digits=8,
                                          decimal_places=3)
    cell_margin_bottom = models.DecimalField(default=56.693, max_digits=8,
                                             decimal_places=3)
    cell_margin_start = models.DecimalField(default=113.389, max_digits=8,
                                            decimal_places=3)
    cell_margin_end = models.DecimalField(default=113.389, max_digits=8,
                                          decimal_places=3)

    # def __str__(self):
    #     if self.theme:
    #         return self.theme.name+' style'
    #     else:
    #         return self.id


class Element(models.Model):
    '''
    Styling for particular elements. If a given field is null, that field will
    revert to table-level styling from the Style model.
    '''
    style = models.ForeignKey(Style,
                              on_delete=models.CASCADE,
                              related_name="elements")

    ELEMENT_TYPE_CHOICES = [
        ("rowHeader", "rowHeader"),
        ("rowSubheader1", "rowSubheader1"),
        ("rowSubheader2", "rowSubheader2"),
        ("rowSubtotal", "rowSubtotal"),
        ("rowNormal1", "rowNormal1"),
        ("rowNormal2", "rowNormal2"),
        ("rowTotal", "rowTotal"),
    ]
    type = models.CharField(max_length=30, choices=ELEMENT_TYPE_CHOICES)

    # Font options
    font_bold = models.BooleanField(blank=True, null=True)
    font_color = models.CharField(max_length=50, blank=True, null=True) #HEX, no hash
    font_italic = models.BooleanField(blank=True, null=True)
    font_name = models.CharField(max_length=50, blank=True, null=True)
    font_size = models.PositiveIntegerField(blank=True, null=True)
    font_small_caps = models.BooleanField(blank=True, null=True)
    font_underline = models.BooleanField(blank=True, null=True)

    # Cell level border color. Sides must be set at table level.
    border_sides = models.CharField(max_length=50, blank=True, null=True) #e.g. "top,bottom,start,end"
    border_color = models.CharField(max_length=50, blank=True, null=True) #HEX, no hash
    border_width = models.PositiveSmallIntegerField(default=1) #pt * 8

    # Cell level background fill for tables.
    background_color = models.CharField(max_length=50, blank=True, null=True) #HEX, no hash

    # Indents and bullets particular element. Designed mostly for "normal"
    bullet_items = models.BooleanField(default=False)

    # Not currently in use - all bullets are hyphens at the moment.
    bullet_style = models.CharField(max_length=50, default="hyphen")

    def __str__(self):
        return self.type


class Structure(models.Model):
    '''
    Controls the format of the table (where things are/how they appear).

    ONE STRUCTURE PER THEME ONLY
    '''
    theme = models.ForeignKey(Theme,
                              on_delete=models.CASCADE,
                              related_name="structures")

    #######
    # General document-level setting
    #######

    # Makes subheaders full width
    full_width_subheader1 = models.BooleanField(default=False)
    full_width_subheader2 = models.BooleanField(default=False)

    #######
    # Fee table only
    #######
    display_alternative_platform = models.BooleanField(default=False)
    # Splits super/investment into two separate setions/tables
    split_platform_types = models.BooleanField(default=False)

    #Orientation options - only for fee tables
    portrait_overflow_limit = models.PositiveSmallIntegerField(default=4)
    landscape_overflow_limit = models.PositiveSmallIntegerField(default=7)
    change_orientation_if_overflow = models.BooleanField(default=True)

    # Control/modify existing content items - fee table only
    display_percentage_subtotal = models.BooleanField(default=False)
    display_percentage_total = models.BooleanField(default=False)
    display_NA_flat_fees = models.BooleanField(default=False)
    display_null_rows = models.BooleanField(default=False)


    # Where the percentage calculation appears in relation to the dollar value.
    POSITION_CHOICES = [
        ("Left", "Left"),
        ("Right", "Right"),
        ("Bottom", "Bottom"),
    ]
    percentage_position = models.CharField(max_length=20,
                                           choices=POSITION_CHOICES,
                                           blank=True, null=True)

    # Not in use
    display_platforms_as_cols = models.BooleanField(default=True)

    #######
    # AA table only
    #######
    hide_variance = models.BooleanField(default=False)
    hide_bar_chart = models.BooleanField(default=False)

    include_cur_vs_rp = models.BooleanField(default=True)
    include_rec_vs_rp = models.BooleanField(default=True)
    include_cur_vs_rp_vs_rec = models.BooleanField(default=True)
    include_cur_vs_rec = models.BooleanField(default=True)

    # Not in use
    hide_risk_profile = models.BooleanField(default=False)


    #######
    # Product table only
    #######
    hide_percentage = models.BooleanField(default=True)
    hide_ICR = models.BooleanField(default=True)

    # These properties are built out because I wrote the doc builder before
    # the front end and didn't want to hard code a table on the front end
    # or recode the whole doc builder.

    # General table properties

    @property
    def general_full_width_subheader1(self):
        return self.full_width_subheader1

    @property
    def general_full_width_subheader2(self):
        return self.full_width_subheader2

    # Fee table properties

    @property
    def fee_display_alternative_platform(self):
        return self.display_alternative_platform

    @property
    def fee_split_platform_types(self):
        return self.split_platform_types

    @property
    def fee_portrait_overflow_limit(self):
        return self.portrait_overflow_limit

    @property
    def fee_landscape_overflow_limit(self):
        return self.landscape_overflow_limit

    @property
    def fee_change_orientation_if_overflow(self):
        return self.change_orientation_if_overflow

    @property
    def fee_display_percentage_subtotal(self):
        return self.display_percentage_subtotal

    @property
    def fee_display_percentage_total(self):
        return self.display_percentage_total

    @property
    def fee_display_NA_flat_fees(self):
        return self.display_NA_flat_fees

    @property
    def fee_display_null_rows(self):
        return self.display_null_rows

    @property
    def fee_percentage_position(self):
        return self.percentage_position

    # AA table properties

    @property
    def aa_hide_variance(self):
        return self.hide_variance

    @property
    def aa_hide_risk_profile(self):
        return self.hide_risk_profile

    @property
    def aa_hide_bar_chart(self):
        return self.hide_bar_chart

    @property
    def aa_include_cur_vs_rp(self):
        return self.include_cur_vs_rp

    @property
    def aa_include_rec_vs_rp(self):
        return self.include_rec_vs_rp

    @property
    def aa_include_cur_vs_rp_vs_rec(self):
        return self.include_cur_vs_rp_vs_rec

    @property
    def aa_include_cur_vs_rec(self):
        return self.include_cur_vs_rec

    # Product table properties

    @property
    def product_hide_percentage(self):
        return self.hide_percentage

    @property
    def product_hide_ICR(self):
        return self.hide_ICR

    class Meta:
        # Each theme must only have one structure.
        constraints = [
            models.UniqueConstraint(fields=['theme'],
                                    name='unique_theme')
        ]

class Content(models.Model):
    '''
    Controls the actual content of the table (i.e. the rows)
    '''
    theme = models.ForeignKey(Theme,
                              on_delete=models.CASCADE,
                              related_name="content",
                              blank=True, null=True)

    # The order of these choices is important - they are created in the order
    # They appear in these lists.
    FEE_CHOICES = [
        ("Status", "Status"),
        ("Product", "Product"),
        ("Balance", "Balance"),
        ("Investments", "Investments"),
        ("One-off Fees Subheader", "One-off Fees Subheader"),
        ("Switch Fees", "Switch Fees"),
        ("Buy/Sell Fees", "Buy/Sell Fees"),
        ("One-off Subtotal", "One-off Subtotal"),
        ("Ongoing Fees Subheader", "Ongoing Fees Subheader"),
        ("Ongoing Fees Content", "Ongoing Fees Content"),
        ("Subtotal", "Subtotal"),
        ("Adviser Fee", "Adviser Fee"),
        ("Total", "Total"),
        ("Aggregated Total", "Aggregated Total"),
        ("AA Summary", 'AA Summary'),
    ]
    AA_CHOICES = [
        ("Status", "Status"),
        ("Defensive Subheader", "Defensive Subheader"),
        ("Defensive Content", "Defensive Content"),
        ("Defensive Subtotal", "Defensive Subtotal"),
        ("Growth Subheader", "Growth Subheader"),
        ("Growth Content", "Growth Content"),
        ("Growth Subtotal", "Growth Subtotal"),
        ("Alternative Subheader", "Alternative Subheader"),
        ("Alternative Content", "Alternative Content"),
        ("Alternative Subtotal", "Alternative Subtotal"),
        ("Total", "Total")
    ]
    PRODUCT_CHOICES = [
        ("Description", "Description"),
        ("Platform Subheader", "Platform Subheader"),
        ("Platform Content", "Defensive Content"),
        ("Platform Subtotal", "Defensive Subtotal"),
        ("Total", "Total")
    ]
    # Excludes a "brokerage" row for now. Limited use cases.
    CONTENT_TYPE_CHOICES = FEE_CHOICES + AA_CHOICES + PRODUCT_CHOICES
    type = models.CharField(max_length=50,
                            choices=CONTENT_TYPE_CHOICES,)

    name = models.CharField(max_length=30, blank=True, null=True)
    visible = models.BooleanField(default=True)

    TABLE_TYPE_CHOICES = [
        ("Product", "Product Advice Table"),
        ("Actual", "Fee Table"),
        ("Consolidated", "Consolidated Fee Table"),
        ("AA", "Asset Allocation Table"),
    ]
    table_type = models.CharField(max_length=20,
                                  choices=TABLE_TYPE_CHOICES)

    element = models.ForeignKey(Element,
                                on_delete=models.SET_NULL,
                                related_name="content",
                                blank=True, null=True)

    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('order',)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.type
