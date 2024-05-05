from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder
from django.db.models import Avg, F, ExpressionWrapper, fields
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    current_date = timezone.now()
    # Calculate and update On-Time Delivery 
    if instance.status == 'completed' and instance.delivery_date <= current_date:
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivery_rate = (completed_pos.filter(delivery_date__lte=current_date).count() /
                                 completed_pos.count()) * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate

    # Update Quality Rating Average
    if instance.quality_rating is not None:
        completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg
    # Save changes to vendor profile
    vendor.save()
@receiver(pre_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date is not None:
        completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, acknowledgment_date__isnull=False)
        avg_response_time = completed_pos.annotate(
            response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        ).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
        instance.vendor.average_response_time = avg_response_time.total_seconds()

    # Update Fulfilment Rate
    if instance.acknowledgment_date is None :
        total_pos = PurchaseOrder.objects.filter(vendor=instance.vendor).count()
        completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
        fulfilment_rate = (completed_pos / total_pos) * 100
        instance.vendor.fulfillment_rate = fulfilment_rate

    # Save changes to vendor profile
    instance.vendor.save()

def temporarily_disable_signals():
    # Temporary disconnect signal handlers
    post_save.disconnect(update_vendor_metrics, sender=PurchaseOrder)
    pre_save.disconnect(update_average_response_time, sender=PurchaseOrder)

def reconnect_signals():
    # Reconnect signal handlers
    post_save.connect(update_vendor_metrics, sender=PurchaseOrder)
    pre_save.connect(update_average_response_time, sender=PurchaseOrder)
