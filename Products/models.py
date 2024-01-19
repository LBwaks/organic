import hashlib
import random
import time
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.postgres.search import SearchVectorField, SearchVector

# from django.db.models.functions import Concat
# from django.db.models import Value
from .choices import RATINGS
from django.db.models import Avg, Count

# Create your models here.


class Category(models.Model):
    """Model definition for Category."""

    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50)
    slug = AutoSlugField(populate_from="name")
    description = RichTextField()
    is_published = models.BooleanField(_("Published"), default=True)
    is_featured = models.BooleanField(_("Featured"), default=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name


class Tag(models.Model):
    """Model definition for Tag."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=50)
    slug = AutoSlugField(populate_from="name")
    category = models.ForeignKey(Category, verbose_name=_(""), on_delete=models.CASCADE)
    description = RichTextField()
    is_published = models.BooleanField(_("Published"), default=True)
    is_featured = models.BooleanField(_("Featured"), default=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        """Unicode representation of Tag."""
        return self.name


class ProductDiscount(models.Model):
    """Model definition for ProductDiscount."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    discount = models.DecimalField(
        _("Percentage Discount"), max_digits=4, decimal_places=2
    )
    start_time = models.DateTimeField(
        _("Discount Start Time"), auto_now=False, auto_now_add=False
    )
    end_time = models.DateTimeField(
        _("Discount End TimeS"), auto_now=False, auto_now_add=False
    )
    created = models.DateTimeField(_(""), auto_now_add=True)

    class Meta:
        """Meta definition for ProductDiscount."""

        verbose_name = "ProductDiscount"
        verbose_name_plural = "ProductDiscounts"

    def __str__(self):
        """Unicode representation of ProductDiscount."""
        return str(self.discount)


class Product(models.Model):
    """Model definition for Product."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    product_reference = models.CharField(_("Reference"), unique=True, max_length=50)
    title = models.CharField(_("Title"), max_length=50)
    slug = AutoSlugField(populate_from="title")
    category = models.ForeignKey(
        Category,
        related_name="product_category",
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
    )
    tag = models.ManyToManyField(Tag, verbose_name=_("Tag"))
    description = RichTextField()
    unit = models.CharField(_("Unit"), max_length=50)
    price = models.IntegerField(_("Price"))
    percentage_discount = models.ForeignKey(
        ProductDiscount,
        related_name="percentage_discount",
        blank=True,
        null=True,
        verbose_name=_("Discount (%)"),
        default=0,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(_("Quantity"))
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(_(""), auto_now=True, auto_now_add=False)

    search_vector = SearchVectorField(null=True, editable=False)
    search_rank = models.FloatField(null=True, editable=False)

    class Meta:
        """Meta definition for Product."""

        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        """Unicode representation of Product."""
        return self.title

    def save(self, *args, **kwargs):
        """Save method for Product."""
        # self.search_vector = (
        #     SearchVector("title")
        #     + SearchVector("category__name")
        #     + SearchVector("tag__name")
        #     + SearchVector("description")
        # )
        #     Concat("category__name", Value(" "), "title"),
        #     Concat('tag__name', Value(' '), 'title'),
        #     "description",
        # )
        # self.search_vector = SearchVector(
        #     "title",
        #     Concat("category__name", Value(" "), "title"),
        #     Concat("tag__name", Value(" "), "title"),
        #     "description",
        # )
        if not self.product_reference:
            self.product_reference = self.generate_unique_id()
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Product."""
        return reverse("product-details", kwargs={"slug": self.slug})

    @property
    def average_rating(self):
        rating = Rating.objects.filter(product=self).aggregate(average=Avg("ratings"))
        avg = rating["average"] or 0
        return float(avg)

    @property
    def ratingCounter(self):
        ratings = (
            Rating.objects.filter(product=self)
            .values("ratings")
            .annotate(count=Count("ratings"))
        )
        # Construct a dictionary to hold the counts
        rating_counts = {rating["ratings"]: rating["count"] for rating in ratings}

        # Return the dictionary containing counts for each star rating
        return rating_counts

    # TODO: Define custom methods here
    def generate_unique_id(self):
        timestamp = int(time.time() * 1000)
        random_num = random.randint(100000, 999999)
        unique_id = f"{timestamp}{random_num}"
        hashed__id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
        return hashed__id


class ProductImage(models.Model):
    """Model definition for ProductImage."""

    # TODO: Define fields here
    product = models.ForeignKey(
        Product,
        related_name="product_image",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        _("Product Image"),
        upload_to="products/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    class Meta:
        """Meta definition for ProductImage."""

        verbose_name = "ProductImage"
        verbose_name_plural = "ProductImages"

    def __str__(self):
        """Unicode representation of ProductImage."""
        return self.product.title


class Rating(models.Model):
    """Model definition for Rating."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        related_name="product_ratings",
        on_delete=models.CASCADE,
    )
    title = models.CharField(_("Subject"), max_length=50)
    ratings = models.IntegerField(_("Ratings"), choices=RATINGS, max_length=50)
    review = models.TextField(_("Review"))
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Rating."""

        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        """Unicode representation of Rating."""
        return f"{self.product} has {self.ratings} ratings"
