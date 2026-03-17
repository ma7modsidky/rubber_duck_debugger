from django.shortcuts import render, get_object_or_404
from .models import DebugLog
from .services.ai_handler import ErrorAnalyzerService

def debugger_home(request, log_id=None):
    # Always fetch history for the sidebar
    history = DebugLog.objects.all().order_by('-created_at')[:15]
    result = None

    # Scenario A: User clicked a history item (GET with log_id)
    if log_id:
        result = get_object_or_404(DebugLog, id=log_id)

    # Scenario B: User submitted a new error (POST)
    elif request.method == "POST":
        traceback = request.POST.get("traceback")
        if traceback:
            ai_service = ErrorAnalyzerService()
            resolution = ai_service.analyze_traceback(traceback)
            
            clean_title = ai_service.extract_error_title(traceback)
            result = DebugLog.objects.create(
                raw_traceback=traceback,
                ai_resolution=resolution,
                error_message=clean_title
            )

    return render(request, "debugger/home.html", {
        "result": result,
        "history": history
    })