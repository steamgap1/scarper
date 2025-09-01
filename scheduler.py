from apscheduler.schedulers.blocking import BlockingScheduler
from app.services.scraper_service import run_scrapers

def scheduled_job():
    print("Ejecutando tareas de scraping programadas...")
    run_scrapers()
    print("Tareas de scraping finalizadas.")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # Programa la ejecución cada 24 horas
    scheduler.add_job(scheduled_job, 'interval', hours=24)
    
    print("Scheduler iniciado. Presiona Ctrl+C para detener.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
