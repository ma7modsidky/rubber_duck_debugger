from django.shortcuts import render, get_object_or_404, redirect
from .models import DebugLog
from .services.ai_handler import ErrorAnalyzerService

def debugger_home(request, log_id=None):
    # Always fetch history for the sidebar
    history = DebugLog.objects.all().order_by('-created_at')[:15]
    result = None
    
    # Scenario A: User submitted a new error (POST)
    if request.method == "POST":
        traceback = request.POST.get("traceback")
        history_context = "\n".join([f"- {log.error_message}" for log in history])
        if traceback:
            ai_service = ErrorAnalyzerService()
            resolution = ai_service.analyze_traceback(traceback, history_context=history_context)
            
            clean_title = ai_service.extract_error_title(traceback)
            new_log = DebugLog.objects.create(
                raw_traceback=traceback,
                ai_resolution=resolution,
                error_message=clean_title
            )
            # Post-Redirect-Get Pattern: Redirect to the detail view of the new result
            return redirect('log_detail', log_id=new_log.id)

    # Scenario B: User clicked a history item (GET with log_id)
    if log_id:
        result = get_object_or_404(DebugLog, id=log_id)

    
    return render(request, "debugger/home.html", {
        "result": result,
        "history": history
    })