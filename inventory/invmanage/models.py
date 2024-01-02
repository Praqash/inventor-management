from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """

    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("invmanage:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """

    name = models.CharField(verbose_name=_("Product Type"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
    The Product Specification Table contains product
    specifiction or features for the product types.
    """

    # product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    # name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    # class Meta:
    #     verbose_name = _("Product Specification")
    #     verbose_name_plural = _("Product Specifications")

    # def __str__(self):
    #     return self.name

    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table contining all product items.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(
        verbose_name=_("Product Name"),
        help_text=_("Required"),
        max_length=255,
    )
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(
        verbose_name=_("Product visibility"),
        help_text=_("Change product visibility"),
        default=True,
    )


    total_count = models.PositiveIntegerField(
        verbose_name=_("Total Count"),
        help_text=_("Total number of products available"),
        default=0,
    )
    remaining_count = models.PositiveIntegerField(
        verbose_name=_("Remaining Count"),
        help_text=_("Number of products remaining after sales"),
        default=0,
    )

    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("invmanage:product_detail", args=[self.slug])

    def __str__(self):
        return self.name
    


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("value"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("image"),
        help_text=_("Upload a product image"),
        upload_to="images/",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Alturnative text"),
        help_text=_("Please add alturnative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

class ProductAllocation(models.Model):
    """
    Model to track product allocations.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_allocated = models.PositiveIntegerField(
        verbose_name=_("Quantity Allocated"),
        help_text=_("Number of products allocated"),
        default=0,
    )
    allocated_to = models.CharField(
        verbose_name=_("Allocated To"),
        help_text=_("Person or entity to whom the products are allocated"),
        max_length=255,
    )
    allocated_at = models.DateTimeField(_("Allocated At"), auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to update product counts when an allocation is made.
        """
        super().save(*args, **kwargs)
        self.product.remaining_count -= self.quantity_allocated
        self.product.save()

    class Meta:
        verbose_name = _("Product Allocation")
        verbose_name_plural = _("Product Allocations")