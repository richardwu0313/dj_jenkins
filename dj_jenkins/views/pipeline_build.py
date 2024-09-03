import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from dj_jenkins.utils import TimeUtil
from dj_jenkins.utils import PipelineBuildUtil
from dj_jenkins.serializers import PipelineBuildSerializer


class PipelineBuildViewSet(viewsets.ModelViewSet):
    queryset = PipelineBuildUtil.get_pipeline_build_objs()
    serializer_class = PipelineBuildSerializer

    @action(detail=False, methods=["post"], url_path="sync")
    def sync(self, request):
        pipeline_fullnames = request.data.get("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        # build: after build, info can't change, so update always==False
        # force: sync since from next build number when false, sync all when true
        force = request.query_params.get("force", False)
        if isinstance(force, str):
            if force.lower() == "true":
                force = True
            else:
                force = False
        result = PipelineBuildUtil.sync(
            pipeline_fullnames=pipeline_fullnames,
            update=False,
            force=force
        )
        return Response(result)

    @action(detail=False, methods=["get"], url_path="results/year")
    def year_results(self, request):
        year = request.query_params.get("year",
                                        f"{datetime.datetime.now().year}")
        year = int(year)
        pipeline_fullnames = request.query_params.getlist("pipeline_fullnames", [])
        year_dates = TimeUtil.get_year_dates(year=year)
        date_dict = {pipeline: {date: ""} for pipeline in pipeline_fullnames for date in year_dates}
        result = PipelineBuildUtil.get_day_results(
            pipeline_fullnames=pipeline_fullnames,
            year=year,
        )
        for pipeline in date_dict:
            for date in date_dict[pipeline]:
                date_dict[pipeline][date] = result.get(pipeline, {}).get(date, "")
        return Response(date_dict)

    @action(detail=False, methods=["get"], url_path="results/month")
    def month_results(self, request):
        year_month = request.query_params.get("date", f"{datetime.now().year}-{datetime.now().month}")
        year = int(year_month.split("-")[0])
        month = int(year_month.split("-")[1].strip("0"))
        pipeline_fullnames = request.query_params.getlist("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        monthly_dates = TimeUtil.get_year_month_dates(year=year, month=month)
        date_dict = {pipeline: {date: ""} for pipeline in pipeline_fullnames for date in monthly_dates}
        result = PipelineBuildUtil.get_day_results(
            pipeline_fullnames=pipeline_fullnames,
            year=year,
            month=month,
        )
        for piepline in date_dict:
            for date in date_dict[piepline]:
                date_dict[piepline][date] = result.get(piepline, {}).get(date, "")
        return Response(date_dict)

    @action(detail=False, methods=["get"], url_path="results/day")
    def day_results(self, request):
        year_month = request.query_params.get("date",
                                              f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}")
        year = int(year_month.split("-")[0])
        month = int(year_month.split("-")[1].strip("0"))
        day = int(year_month.split("-")[2].strip("0"))
        pipeline_fullnames = request.query_params.getlist("pipeline_fullnames", "")
        pipeline_fullnames = pipeline_fullnames.split(",")
        date_dict = {pipeline: {day: ""} for pipeline in pipeline_fullnames}
        result = PipelineBuildUtil.get_day_results(
            pipeline_fullnames=pipeline_fullnames,
            year=year,
            month=month,
            day=day
        )
        for piepline in date_dict:
            for date in date_dict[piepline]:
                date_dict[piepline][date] = result.get(piepline, {}).get(date, "")
        return Response(date_dict)

