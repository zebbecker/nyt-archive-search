from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.core.mail import EmailMessage, send_mail
from .forms import FullSearchForm, DemoSearchForm
from gatherer.gatherer import gatherer as gatherer
import csv
import os
import pandas as pd
from gatherer.melk_format import melk_fields
from gatherer import config


def index(request):
    return render(request, "gatherer/index.html")


def about(request):
    return render(request, "gatherer/about.html")


def search(request):
    if request.method == "POST":
        form = FullSearchForm(request.POST)
        if form.is_valid():

            context = form.cleaned_data
            df_out = gatherer(
                context["keyword"],
                context["start_date"],
                context["end_date"],
                context["api_key"],
                context["download_limit"],
            )
            context["file_out"] = df_out

            filename_out = (
                '"'
                + form.cleaned_data["keyword"]
                + "_"
                + form.cleaned_data["start_date"].strftime("%Y")
                + "_"
                + form.cleaned_data["end_date"].strftime("%Y")
                + ".csv"
                + '"'
            )

            """ response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=" + filename_out},
            ) 

            df_out.to_csv(path_or_buf=response, sep=";", index=False)
            """
            response = HttpResponse(
                "Request recieved. Your dataset will be sent by email when the search completes."
            )

            email = EmailMessage(
                subject="Archive Search Results Available",
                body="Your search just finished! The collected data is attached to this email. Please do not reply to this address- the inbox is not monitored.",
                from_email=os.environ["DJANGO_EMAIL_USER"],
                to=[form.cleaned_data["user_email"]],
            )

            email.attach(
                filename=filename_out,
                content=df_out.to_csv(sep=";", index=False),
                mimetype="text/csv",
            )

            email.send(fail_silently=False)

            return response

            # return render(request, "gatherer/display_results.html", c)
    else:
        form = FullSearchForm()

    return render(request, "gatherer/search.html", {"form": form})


def demo(request):
    if request.method == "POST":
        form = DemoSearchForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            df_out = gatherer(
                context["keyword"],
                context["start_date"],
                context["end_date"],
                api_key=None,
                download_limit=config.NYT_DEFAULT_LIMIT,
            )
            context["file_out"] = df_out

            filename_out = (
                '"'
                + form.cleaned_data["keyword"]
                + "_"
                + form.cleaned_data["start_date"].strftime("%Y")
                + "_"
                + form.cleaned_data["end_date"].strftime("%Y")
                + ".csv"
                + '"'
            )

            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=" + filename_out},
            )

            df_out.to_csv(path_or_buf=response, sep=";", index=False)

            return response
    else:
        form = DemoSearchForm()

    return render(request, "gatherer/demo.html", {"form": form})


def display_results(request, keyword, start_date, end_date):
    return render(
        request,
        "display_results.html",
        {"keyword": keyword, "start_date": start_date, "end_date": end_date},
    )
