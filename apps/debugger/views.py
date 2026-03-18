from django.shortcuts import render, get_object_or_404, redirect
from .models import DebugLog
from .services.ai_handler import ErrorAnalyzerService
from django.contrib import messages


def debugger_home(request, log_id=None):
    # Always fetch history for the sidebar
    history = DebugLog.objects.all().order_by("-created_at")[:15]
    result = None

    # Scenario A: User submitted a new error (POST)
    if request.method == "POST":
        traceback = request.POST.get("traceback", "").strip()
        ai_service = ErrorAnalyzerService()
        clean_title = ai_service.extract_error_title(traceback)
        # 1. Input Validation: Check for weird/empty text
        # If the extractor couldn't find a specific Python error, reject it
        if clean_title in ["Empty Traceback", "General Python Error"]:
            messages.error(
                request,
                "The input provided does not look like a valid Python traceback.",
            )
            return redirect("home")

        history_context = "\n".join([f"- {log.error_message}" for log in history])

        # 2. Handle Gemini/Network failures
        try:
            resolution = ai_service.analyze_traceback(
                traceback, history_context=history_context
            )
            new_log = DebugLog.objects.create(
                raw_traceback=traceback,
                ai_resolution=resolution,
                error_message=clean_title,
            )
            return redirect("log_detail", log_id=new_log.id)

        except Exception as e:
            # Log the real error for you, but show a nice message to the user
            print(f"AI Service Error: {e}")
            messages.error(
                request,
                "The AI service is currently unavailable or the rate limit was hit. Please try again in a moment.",
            )
            return redirect("home")

    # Scenario B: User clicked a history item (GET with log_id)
    if log_id:
        result = get_object_or_404(DebugLog, id=log_id)

    return render(request, "debugger/home.html", {"result": result, "history": history})
