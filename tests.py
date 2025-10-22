from datetime import datetime

def date_validator():

    while True:
        print("\n" + "="*50)
        print("📅 SISTEMA DE FECHAS DE WESTEROS")
        print("="*50)
        print("• Formato: AÑO-MES-DÍA (ej: 298-3-15)")
        print("• Rango válido: Años 1-400 DC (Después de la Conquista)")
        print("-" * 50)
        
        fecha_str = input("Ingrese fecha: ").strip()
        
        try:
            # Validar con datetime
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
            año = fecha_obj.year
            mes = fecha_obj.month
            dia = fecha_obj.day
            
            # Validar rango de años de Westeros
            if año < 1:
                print("🚫 ERROR: El calendario de Westeros comienza en el año 1 DC")
                print("   (Año de la coronación de Aegon el Conquistador)")
                continue
                
            if año > 400:
                print("🚫 ERROR: Año fuera del rango histórico conocido")
                print("   El planificador cubre hasta el año 400 DC")
                continue
            
            # Éxito - fecha válida
            print("="*50)
            print(f"✅ FECHA VÁLIDA CONFIRMADA")
            print(f"   📅 {dia} del mes {mes} del año {año} DC")
            
            # Contexto histórico
            if año == 1:
                print("   🏰 Año de la coronación de Aegon el Conquistador")
            elif 129 <= año <= 131:
                print("   🐉 Periodo de la Danza de los Dragones")
            elif año == 281:
                print("   🏆 Año del Torneo de Harrenhal")
            elif 298 <= año <= 300:
                print("   ⚔️  Periodo de la Guerra de los Cinco Reyes")
            elif año > 300:
                print("   🔮 Eventos posteriores a los libros conocidos")
                
            print("="*50)
            return año, mes, dia
            
        except ValueError as e:
            error_str = str(e)
            
            if "day is out of range" in error_str:
                print("🚫 ERROR: Día inválido para el mes especificado")
            elif "month must be in 1..12" in error_str:
                print("🚫 ERROR: Mes debe estar entre 1 y 12")
            elif "unconverted data remains" in error_str:
                print("🚫 ERROR: Formato incorrecto - elimine texto adicional")
            elif "does not match format" in error_str:
                print("🚫 ERROR: Formato incorrecto. Use: AÑO-MES-DÍA")
                print("   Ejemplo: '298-3-15' (no '298-03-15')")
            else:
                print(f"🚫 ERROR: {error_str}")