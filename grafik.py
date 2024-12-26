import numpy as np
import matplotlib.pyplot as plt

def find_intersection_points(constraints):
    intersection_points = []
    n = len(constraints)
    
    # Mencari titik potong dengan sumbu y (vertikal) untuk setiap kendala
    for i in range(n):
        a1, b1, c1 = constraints[i]
        if b1 != 0:
            y = c1 / b1
            intersection_points.append((0, y))
    
    # Mencari titik potong dengan sumbu x (horizontal) untuk setiap kendala
    for i in range(n):
        a1, b1, c1 = constraints[i]
        if a1 != 0:
            x = c1 / a1
            intersection_points.append((x, 0))
    
    # Menambahkan titik origin
    intersection_points.append((0, 0))
    
    # Mencari titik potong antar kendala
    for i in range(n):
        a1, b1, c1 = constraints[i]
        for j in range(i + 1, n):
            a2, b2, c2 = constraints[j]
            det = a1 * b2 - a2 * b1
            if det != 0:
                x = (c1 * b2 - c2 * b1) / det
                y = (a1 * c2 - a2 * c1) / det
                if x >= 0 and y >= 0:
                    intersection_points.append((x, y))
    
    return intersection_points

def is_feasible_point(point, constraints):
    x, y = point
    for a, b, c in constraints:
        if a * x + b * y > c + 1e-10:
            return False
    return True

def format_currency(value):
    return f"Rp {value:,.0f}".replace(",", ".")

def format_number(value):
    return int(value) if isinstance(value, float) and value.is_integer() else value

def remove_float_zero(x):
    x_str = str(x)
    return x_str[:-2] if x_str.endswith('.0') else x_str

def print_optimization_table(feasible_points, obj_a, obj_b):
    col_width = {
        'point': 15,
        'func': 35,
        'value': 20
    }
    
    total_width = sum(col_width.values()) + 4
    line = "=" * total_width
    
    print("\n" + line)
    title = "TABEL PERHITUNGAN NILAI FUNGSI TUJUAN PADA TITIK POJOK"
    print(f"{title:^{total_width}}")
    print(line)
    
    headers = [
        f"{'Titik Pojok':^{col_width['point']}}",
        f"{'Fungsi Tujuan':^{col_width['func']}}",
        f"{'Nilai Z':^{col_width['value']}}"
    ]
    print(f"|{headers[0]}|{headers[1]}|{headers[2]}|")
    print("-" * total_width)
    
    max_value = float('-inf')
    optimal_point = None
    
    # Mengurutkan titik-titik berdasarkan koordinat y
    sorted_points = sorted(feasible_points, key=lambda p: (-p[1], p[0]))
    
    origin_point = None
    other_points = []
    for point in sorted_points:
        if point[0] == 0 and point[1] == 0:
            origin_point = point
        else:
            other_points.append(point)
            
    final_points = (other_points[:2] + [origin_point] + other_points[2:]) if len(other_points) >= 2 and origin_point is not None else sorted_points
    
    # Mencetak setiap baris
    for i, point in enumerate(final_points):
        x, y = point
        z_value = obj_a * x + obj_b * y
        
        # Format fungsi tujuan 
        if x == 0 and y == 0:
            func_str = f"{remove_float_zero(obj_a)}(0) + {remove_float_zero(obj_b)}(0)"
        else:
            terms = []
            if obj_a != 0:
                terms.append(f"{remove_float_zero(obj_a)}({remove_float_zero(x)})")
            if obj_b != 0:
                terms.append(f"{remove_float_zero(obj_b)}({remove_float_zero(y)})")
            func_str = " + ".join(terms)
        
        # Format titik pojok dengan huruf
        point_label = f"{chr(65 + i)}({remove_float_zero(x)},{remove_float_zero(y)})"
        formatted_z = format_currency(z_value)
        
        # Mencetak baris dengan format yang tepat
        row = [
            f"{point_label:<{col_width['point']}}",
            f"{func_str:<{col_width['func']}}",
            f"{formatted_z:>{col_width['value']}}"
        ]
        print(f"|{row[0]}|{row[1]}|{row[2]}|")
        
        if z_value > max_value:
            max_value = z_value
            optimal_point = point
    
    print(line)
    
    # Menampilkan kesimpulan 
    print("\n\nKESIMPULAN:")
    print("-" * total_width)
    x_opt, y_opt = optimal_point
    print(f"Solusi optimal dicapai pada titik ({remove_float_zero(x_opt)}, {remove_float_zero(y_opt)})")
    print(f"dengan rincian:")
    print(f"- X1 (produk 1) = {remove_float_zero(x_opt)} unit")
    print(f"- X2 (produk 2) = {remove_float_zero(y_opt)} unit")
    print(f"Nilai fungsi tujuan optimal (Z) = {format_currency(max_value)}")

def plot_feasible_region():
    print("Masukkan fungsi tujuan:")
    obj_a = float(input("Masukkan koefisien x1 untuk fungsi tujuan: "))
    obj_b = float(input("Masukkan koefisien x2 untuk fungsi tujuan: "))

    num_constraints = int(input("\nBerapa jumlah kendala yang ingin dimasukkan? "))
    constraints = []

    for i in range(num_constraints):
        print(f"\nMasukkan kendala ke-{i+1}:")
        a = float(input(f"Masukkan koefisien x1 untuk kendala {i+1}: "))
        b = float(input(f"Masukkan koefisien x2 untuk kendala {i+1}: "))
        c = float(input(f"Masukkan konstanta kendala {i+1}: "))
        constraints.append((a, b, c))

    # Mencari titik-titik perpotongan
    intersection_points = find_intersection_points(constraints)
    
    # Mencari titik-titik yang feasible
    feasible_points = [point for point in intersection_points if is_feasible_point(point, constraints)]

    # Membuat tabel optimasi
    print_optimization_table(feasible_points, obj_a, obj_b)

    x_vals = np.linspace(0, 150, 150)
    plt.figure(figsize=(10, 6))

    for i, (a, b, c) in enumerate(constraints):
        y_vals = (c - a * x_vals) / b
        plt.plot(x_vals, y_vals, label=f"Kendala {i+1}: {remove_float_zero(a)}x1 + {remove_float_zero(b)}x2 <= {remove_float_zero(c)}")

    plt.fill_between(x_vals, 0, np.minimum.reduce([(c - a * x_vals) / b for (a, b, c) in constraints]), 
                     where=(x_vals >= 0) & (x_vals <= 150), color='gray', alpha=0.3, label="Daerah Feasible")

    # Plot titik-titik feasible
    x_points = [point[0] for point in feasible_points]
    y_points = [point[1] for point in feasible_points]
    plt.scatter(x_points, y_points, color='red', zorder=5, label='Titik Pojok')

    plt.xlim(0, 150)
    plt.ylim(0, 150)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Optimasi Linear Programming dengan Metode Grafik")
    plt.legend(loc="best")
    plt.grid(True)

    # Plot fungsi tujuan
    slope = -obj_a / obj_b
    intercept = 0
    y_vals_obj = slope * x_vals + intercept
    plt.plot(x_vals, y_vals_obj, label=f"Fungsi Tujuan: {remove_float_zero(obj_a)}x1 + {remove_float_zero(obj_b)}x2", color='green', linestyle='--')

    plt.show()

def main():
    plot_feasible_region()

if __name__ == "__main__":
    main()