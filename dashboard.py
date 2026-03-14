import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(20, 26))
fig.patch.set_facecolor('#0F1923')
fig.suptitle('CLÍNICA DEL PACÍFICO — Panel de Indicadores', 
             fontsize=22, fontweight='bold', color='white', y=0.98)

# ── COLORES ────────────────────────────────────────────────────────────────────
BG     = '#162030'
AZUL   = '#2E86DE'
VERDE  = '#1BC98E'
NARANJ = '#F9A825'
ROJO   = '#E74C3C'
VIOLA  = '#8B5CF6'
TEAL   = '#06B6D4'
BLANCO = '#EFF3F8'
GRIS   = '#8A9BB0'

def ax_style(ax, title):
    ax.set_facecolor(BG)
    ax.set_title(title, color=BLANCO, fontsize=11, fontweight='bold', pad=10, loc='left')
    ax.tick_params(colors=GRIS, labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#253545')
    ax.spines['bottom'].set_color('#253545')
    ax.grid(color='#253545', linewidth=0.5)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 1 — KPIs como tabla de texto
# ══════════════════════════════════════════════════════════════════════════════
ax_kpi = fig.add_axes([0.03, 0.87, 0.94, 0.09])
ax_kpi.set_facecolor(BG)
ax_kpi.axis('off')
ax_kpi.set_title('KPIs Ejecutivos', color=BLANCO, fontsize=11,
                 fontweight='bold', pad=6, loc='left')

kpis = [
    ("Pacientes/día", "184",    "+12%",     VERDE),
    ("Ocupación camas","78%",   "meta 75-85%", AZUL),
    ("Satisfacción",  "87%",    "+4 pts",    VERDE),
    ("Tiempo espera", "23 min", "meta 20",   ROJO),
    ("Ingresos mes",  "$284k",  "+8.5%",     VERDE),
    ("Readmisiones",  "4.2%",   "meta <3%",  ROJO),
    ("Cirugías cancel","3.8%",  "meta <2%",  ROJO),
    ("Ausentismo",    "3.1%",   "meta <4%",  VERDE),
]

n = len(kpis)
for i, (label, valor, nota, color) in enumerate(kpis):
    x = i / n
    # fondo de tarjeta
    rect = plt.Rectangle((x + 0.002, 0.02), 1/n - 0.008, 0.94,
                          facecolor='#1C2B3A', transform=ax_kpi.transAxes,
                          clip_on=True)
    ax_kpi.add_patch(rect)
    # borde de color
    from matplotlib.lines import Line2D
    lx = x + 0.003
    ax_kpi.add_line(Line2D([lx, lx], [0.08, 0.92],
                           transform=ax_kpi.transAxes, color=color, linewidth=3))
    cx = x + 1/(2*n)
    ax_kpi.text(cx, 0.72, valor,  ha='center', va='center', fontsize=14,
                fontweight='bold', color=BLANCO, transform=ax_kpi.transAxes)
    ax_kpi.text(cx, 0.44, label,  ha='center', va='center', fontsize=8,
                color=GRIS, transform=ax_kpi.transAxes)
    ax_kpi.text(cx, 0.18, nota,   ha='center', va='center', fontsize=8,
                color=color, transform=ax_kpi.transAxes)

# ══════════════════════════════════════════════════════════════════════════════
# FILA 2 — Consultas por especialidad + Ocupación camas
# ══════════════════════════════════════════════════════════════════════════════
ax1 = fig.add_axes([0.03, 0.66, 0.44, 0.18])
ax_style(ax1, 'Consultas por especialidad (mes)')

especialidades = ['Medicina interna', 'Pediatría', 'Ginecología',
                  'Traumatología', 'Cirugía general', 'Cardiología']
consultas = [328, 284, 240, 200, 168, 140]
colores_esp = [AZUL, VERDE, VIOLA, NARANJ, ROJO, TEAL]

bars = ax1.barh(especialidades, consultas, color=colores_esp, height=0.6)
ax1.set_xlim(0, 400)
ax1.set_xlabel('Nº consultas', color=GRIS, fontsize=9)
ax1.tick_params(axis='y', labelcolor=BLANCO)
for bar, val in zip(bars, consultas):
    ax1.text(val + 5, bar.get_y() + bar.get_height()/2,
             str(val), va='center', color=GRIS, fontsize=9)

ax2 = fig.add_axes([0.53, 0.66, 0.44, 0.18])
ax_style(ax2, 'Ocupación de camas por unidad (%)')

pisos = ['UCI', 'Maternidad', 'Médico', 'Quirúrgico', 'Pediatría']
ocup  = [90, 80, 78, 72, 65]
col_c = [ROJO, NARANJ, AZUL, VIOLA, VERDE]

bars2 = ax2.barh(pisos, ocup, color=col_c, height=0.6)
ax2.axvline(x=85, color=NARANJ, linestyle='--', linewidth=1.5, label='Máx 85%')
ax2.axvline(x=75, color=VERDE,  linestyle='--', linewidth=1.5, label='Mín 75%')
ax2.set_xlim(0, 110)
ax2.set_xlabel('Ocupación (%)', color=GRIS, fontsize=9)
ax2.tick_params(axis='y', labelcolor=BLANCO)
ax2.legend(fontsize=8, facecolor='#1C2B3A', edgecolor='#253545',
           labelcolor=GRIS, loc='lower right')
for bar, val in zip(bars2, ocup):
    ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val}%', va='center', color=BLANCO, fontsize=9, fontweight='bold')

# ══════════════════════════════════════════════════════════════════════════════
# FILA 3 — Ingresos por servicio + Tendencia ingresos
# ══════════════════════════════════════════════════════════════════════════════
ax3 = fig.add_axes([0.03, 0.45, 0.44, 0.17])
ax_style(ax3, 'Ingresos por servicio ($k)')

servicios  = ['Hospitalización', 'Cirugías', 'Consulta externa',
              'Imágenes/Lab.', 'Procedimientos']
ingresos_s = [98, 79, 60, 41, 16]
col_ing    = [AZUL, VIOLA, VERDE, NARANJ, TEAL]

bars3 = ax3.bar(servicios, ingresos_s, color=col_ing, width=0.55)
ax3.set_ylabel('Miles USD', color=GRIS, fontsize=9)
ax3.tick_params(axis='x', labelcolor=BLANCO, labelsize=8, rotation=15)
for bar, val in zip(bars3, ingresos_s):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 1,
             f'${val}k', ha='center', va='bottom', color=BLANCO,
             fontsize=9, fontweight='bold')

ax4 = fig.add_axes([0.53, 0.45, 0.44, 0.17])
ax_style(ax4, 'Tendencia de ingresos — últimos 6 meses ($k)')

meses = ['Oct', 'Nov', 'Dic', 'Ene', 'Feb', 'Mar']
tend  = [221, 249, 261, 270, 262, 284]
x_t   = np.arange(len(meses))

ax4.fill_between(x_t, tend, alpha=0.2, color=AZUL)
ax4.plot(x_t, tend, color=AZUL, linewidth=2.5,
         marker='o', markersize=8,
         markerfacecolor='#0F1923', markeredgecolor=AZUL, markeredgewidth=2)
ax4.set_xticks(x_t)
ax4.set_xticklabels(meses, color=BLANCO)
ax4.set_ylim(200, 305)
ax4.set_ylabel('Miles USD', color=GRIS, fontsize=9)
for xi, yi in zip(x_t, tend):
    ax4.text(xi, yi + 4, f'${yi}k', ha='center', color=BLANCO,
             fontsize=8, fontweight='bold')

# ══════════════════════════════════════════════════════════════════════════════
# FILA 4 — Indicadores clínicos + Personal
# ══════════════════════════════════════════════════════════════════════════════
ax5 = fig.add_axes([0.03, 0.24, 0.44, 0.17])
ax_style(ax5, 'Indicadores de calidad clínica (%)')

indicadores = ['Adherencia protocolos', 'Dx correcto',
               'Satisfacción paciente', 'Consentim. digital']
vals_clin  = [91, 94, 87, 60]
metas_clin = [90, 90, 85, 80]
col_clin   = [VERDE if v >= m else ROJO
              for v, m in zip(vals_clin, metas_clin)]

x_c = np.arange(len(indicadores))
bars_c = ax5.bar(x_c, vals_clin, color=col_clin, width=0.4, label='Valor real', alpha=0.9)
ax5.scatter(x_c, metas_clin, color=BLANCO, zorder=5, s=60,
            marker='_', linewidths=3, label='Meta')
ax5.set_xticks(x_c)
ax5.set_xticklabels(indicadores, color=BLANCO, fontsize=8, rotation=10)
ax5.set_ylim(0, 110)
ax5.set_ylabel('%', color=GRIS, fontsize=9)
ax5.legend(fontsize=8, facecolor='#1C2B3A', edgecolor='#253545',
           labelcolor=GRIS)
for bar, val in zip(bars_c, vals_clin):
    ax5.text(bar.get_x() + bar.get_width()/2, val + 1,
             f'{val}%', ha='center', va='bottom', color=BLANCO,
             fontsize=9, fontweight='bold')

ax6 = fig.add_axes([0.53, 0.24, 0.44, 0.17])
ax_style(ax6, 'Distribución del personal (218 total)')

personal_cats = ['Enfermería\n92', 'Médicos\n68',
                 'Técnicos\n36', 'Administrativo\n22']
personal_vals = [92, 68, 36, 22]
col_per = [VERDE, AZUL, VIOLA, TEAL]

bars6 = ax6.bar(personal_cats, personal_vals, color=col_per, width=0.5)
ax6.set_ylabel('Personas', color=GRIS, fontsize=9)
ax6.tick_params(axis='x', labelcolor=BLANCO, labelsize=9)
for bar, val in zip(bars6, personal_vals):
    ax6.text(bar.get_x() + bar.get_width()/2, val + 1,
             str(val), ha='center', va='bottom', color=BLANCO,
             fontsize=11, fontweight='bold')

# ══════════════════════════════════════════════════════════════════════════════
# FILA 5 — Panel de alertas
# ══════════════════════════════════════════════════════════════════════════════
ax7 = fig.add_axes([0.03, 0.04, 0.94, 0.17])
ax7.set_facecolor(BG)
ax7.axis('off')
ax7.set_title('Panel de Alertas — Situaciones que requieren acción',
              color=BLANCO, fontsize=11, fontweight='bold', pad=8, loc='left')

alertas = [
    (ROJO,   'CRÍTICO',  'UCI al 90% capacidad (18/20 camas ocupadas)'),
    (ROJO,   'CRÍTICO',  'Neurología: tiempo espera 36 min (meta 30 min)'),
    (ROJO,   'CRÍTICO',  'Cirugías canceladas 3.8% (meta <2%)'),
    (NARANJ, 'ATENCIÓN', 'Readmisiones 30d: 4.2% (meta <3%)'),
    (NARANJ, 'ATENCIÓN', 'Cuentas por cobrar vencidas: $54k (+30 días)'),
    (NARANJ, 'ATENCIÓN', 'Tiempo espera imágenes: 47 min (meta 30 min)'),
    (NARANJ, 'ATENCIÓN', 'Satisfacción laboral: 72% (meta 80%)'),
    (VERDE,  'OK',       'Infecciones nosocomiales: 1.8% (meta <2%)'),
    (VERDE,  'OK',       'Mortalidad intrahospitalaria: 0.9% (bench 1.1%)'),
    (VERDE,  'OK',       'Adherencia a protocolos clínicos: 91%'),
]

cols  = 2
rows  = 5
for i, (color, nivel, msg) in enumerate(alertas):
    col_i = i // rows
    row_i = i % rows
    x = 0.01 + col_i * 0.50
    y = 0.82 - row_i * 0.17
    # fondo
    rect = plt.Rectangle((x, y - 0.05), 0.48, 0.14,
                          facecolor=color, alpha=0.12,
                          transform=ax7.transAxes, clip_on=False)
    ax7.add_patch(rect)
    ax7.text(x + 0.01, y + 0.02, '●', color=color, fontsize=10,
             transform=ax7.transAxes, va='center')
    ax7.text(x + 0.04, y + 0.02, f'[{nivel}]', color=color, fontsize=8,
             fontweight='bold', transform=ax7.transAxes, va='center')
    ax7.text(x + 0.13, y + 0.02, msg, color=BLANCO, fontsize=8,
             transform=ax7.transAxes, va='center')

# ── Pie de página ──────────────────────────────────────────────────────────────
fig.text(0.03, 0.01,
         'Clínica del Pacífico  |  Plan de Transformación Digital  |  Marzo 2026',
         fontsize=8, color=GRIS)
fig.text(0.97, 0.01, 'Python / Matplotlib', fontsize=8, color=GRIS, ha='right')

plt.savefig('dashboard_clinica_pacifico.png', dpi=150, bbox_inches='tight',
            facecolor='#0F1923')
plt.show()
print("Dashboard guardado como: dashboard_clinica_pacifico.png")
