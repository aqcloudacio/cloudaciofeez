from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, get_list_or_404

from investments.models import Investment, AssetAllocation
from portfolios.models import Portfolio, ModelInvestment
#

@receiver(pre_save, sender=Portfolio)
def clone_portfolio(sender, instance, *args, **kwargs):
    '''
    Searches for a template portfolio of the same name where template = True.
    Once found, the instance is updated with that template's details.
    '''
    if not instance.id and not instance.template and not instance.auto_created:
        platform = instance.platform
        model_value = instance.model_value
        template_id = instance.template_id
        portfolio_template = get_object_or_404(Portfolio,
                                               id=instance.template_id,
                                               template=True)
        instance.__dict__.update(portfolio_template.__dict__)

        instance.id = None

        instance.template_id = template_id
        instance.model_value = model_value
        instance.platform = platform
        instance.template = False
    print(instance)


@receiver(post_save, sender=Portfolio)
def clone_portfolio_model(sender, instance, *args, **kwargs):
    '''
    Clones the model investment parameters for model portfolios. Also creates
    individual investments that belong to the model and assigns them a value.
    '''
    if not instance.template and not instance.model_investments.exists() and not instance.auto_created:
        try:
            model_investment_list = get_list_or_404(ModelInvestment,
                                                    portfolio=instance.template_id)
        except Exception as e:
            print(e)
            model_investment_list = None

        if model_investment_list:
            for model in model_investment_list:
                # Clones the model to the new portfolio
                new_model_object = ModelInvestment()
                new_id = new_model_object.id
                new_model_object.__dict__.update(model.__dict__)
                new_model_object.portfolio = instance
                new_model_object.id = new_id
                new_model_object.save()

                # Creates investments based off the model.
                model_amount = model.percentage*instance.model_value
                new_model_investment = Investment(name=model.investment_name,
                                                  portfolio=instance,
                                                  platform=instance.platform,
                                                  amount=model_amount)
                new_model_investment.save()
