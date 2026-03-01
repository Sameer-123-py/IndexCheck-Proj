from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .services.excel_processor import ExcelLLMProcessor
import os
import logging

logger = logging.getLogger(__name__)

def upload_excel(request):
    context = {}
    
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        fs = FileSystemStorage()
        filename = fs.save(excel_file.name, excel_file)
        file_path = fs.path(filename)
        
        try:
            # Create processor and run
            processor = ExcelLLMProcessor(file_path)
            output_file, processed_data, stats = processor.run()
            
            if output_file and stats:
                context = {
                    'success': True,
                    'download_ready': True,
                    'download_path': fs.url(os.path.basename(output_file)),
                    'total_rows': stats['total_rows'],
                    'processed_rows': stats['processed'],
                    'skipped_rows': stats['skipped'],
                    'error_rows': stats['errors'],
                    'success_rate': f"{(stats['processed']/stats['total_rows']*100):.1f}" if stats['total_rows'] > 0 else 0,
                    'processed_data': processed_data,  # Preview data
                }
            else:
                context = {'error': 'Processing failed. Check logs.'}
            
        except Exception as e:
            logger.error(f"Error in upload_excel: {str(e)}")
            context = {'error': f"Error processing file: {str(e)}"}
    
    return render(request, 'upload.html', context)