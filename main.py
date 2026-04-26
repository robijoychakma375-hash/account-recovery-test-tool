#!/usr/bin/env python3
"""
Account Recovery Testing Tool
Authorized demo/test environment only
"""

import click
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from input.file_processor import FileProcessor
from core.processor import AccountRecoveryProcessor
from output.terminal_output import TerminalOutput, console
from output.report_generator import ReportGenerator
from database.models import init_db
from database.seed_data import seed_demo_accounts

@click.group()
def cli():
    """Account Recovery Testing Tool"""
    pass

@cli.command()
@click.option('-f', '--file', 'input_file', required=True, help='Input file (TXT, CSV, XLSX)')
@click.option('-o', '--output', 'output_format', type=click.Choice(['csv', 'excel', 'json', 'all']), default='csv', help='Output format')
@click.option('--show-otp', is_flag=True, help='Display OTP codes in terminal')
@click.option('--generic-response', is_flag=True, help='Use generic responses (no account enumeration)')
def process(input_file, output_format, show_otp, generic_response):
    """Process identifiers from input file"""
    try:
        # Print header
        TerminalOutput.print_header()
        
        # Load and validate input file
        TerminalOutput.print_info(f"Reading file: {input_file}")
        identifiers, skipped = FileProcessor.read_file(input_file)
        TerminalOutput.print_success(f"Loaded {len(identifiers)} identifiers (skipped {skipped} invalid lines)")
        
        # Remove duplicates
        identifiers, duplicates = FileProcessor.remove_duplicates(identifiers)
        if duplicates > 0:
            TerminalOutput.print_warning(f"Removed {duplicates} duplicate entries")
        
        # Initialize processor
        processor = AccountRecoveryProcessor()
        progress = TerminalOutput.create_progress_bar()
        
        # Process identifiers
        with progress:
            task = progress.add_task(
                "[cyan]Processing...",
                total=len(identifiers),
                status="Starting"
            )
            
            for idx, identifier in enumerate(identifiers):
                result = processor.process(identifier)
                
                # Print status
                if show_otp:
                    TerminalOutput.print_status(result.identifier, result.status, result.message, result.otp_code)
                else:
                    TerminalOutput.print_status(result.identifier, result.status, result.message)
                
                progress.update(task, advance=1, status=result.status)
        
        # Print summary
        summary = processor.get_summary()
        TerminalOutput.print_summary(summary)
        
        # Generate reports
        TerminalOutput.print_info("Generating reports...")
        
        reports_generated = []
        if output_format in ['csv', 'all']:
            csv_file = ReportGenerator.generate_csv_report(processor.get_results())
            reports_generated.append(('CSV', csv_file))
        
        if output_format in ['excel', 'all']:
            excel_file = ReportGenerator.generate_excel_report(processor.get_results())
            reports_generated.append(('Excel', excel_file))
        
        if output_format in ['json', 'all']:
            json_file = ReportGenerator.generate_json_report(processor.get_results())
            reports_generated.append(('JSON', json_file))
        
        # Print report locations
        console.print("\n[bold cyan]Reports Generated:[/bold cyan]")
        for fmt, file_path in reports_generated:
            console.print(f"  ✓ {fmt}: {file_path}")
        
        processor.close()
        TerminalOutput.print_success("Processing completed!")
        
    except Exception as e:
        TerminalOutput.print_error(str(e))
        sys.exit(1)

@cli.command()
def init():
    """Initialize database and seed demo data"""
    try:
        TerminalOutput.print_info("Initializing database...")
        init_db()
        TerminalOutput.print_success("Database initialized")
        
        seed_demo_accounts()
        TerminalOutput.print_success("Demo accounts seeded")
        
    except Exception as e:
        TerminalOutput.print_error(str(e))
        sys.exit(1)

@cli.command()
@click.option('-i', '--identifier', required=True, help='Phone or email to test')
@click.option('--show-otp', is_flag=True, help='Display OTP code')
def test(identifier, show_otp):
    """Test single identifier"""
    try:
        TerminalOutput.print_header()
        
        processor = AccountRecoveryProcessor()
        result = processor.process(identifier)
        
        if show_otp:
            TerminalOutput.print_status(result.identifier, result.status, result.message, result.otp_code)
        else:
            TerminalOutput.print_status(result.identifier, result.status, result.message)
        
        # Print detailed result
        console.print("\n[bold cyan]Result Details:[/bold cyan]")
        console.print(f"  Type: {result.input_type}")
        console.print(f"  Status: {result.status}")
        console.print(f"  Message: {result.message}")
        if result.error:
            console.print(f"  Error: {result.error}")
        if result.otp_code:
            console.print(f"  OTP: {result.otp_code}")
        
        processor.close()
        
    except Exception as e:
        TerminalOutput.print_error(str(e))
        sys.exit(1)

if __name__ == '__main__':
    cli()
