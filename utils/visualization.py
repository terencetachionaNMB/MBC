import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Brand colors
NAVY_BLUE = '#003366'
GOLD = '#FFD700'
LIGHT_BLUE = '#4A90E2'
LIGHT_GOLD = '#FFE55C'
GRAY = '#666666'
LIGHT_GRAY = '#E0E0E0'

class VisualizationHelper:
    """
    Centralized visualization utilities using Plotly with brand colors.
    """
    
    @staticmethod
    def get_color_palette():
        """Return brand color palette"""
        return [NAVY_BLUE, GOLD, LIGHT_BLUE, LIGHT_GOLD, '#1E5A8E', '#FFC700', '#6BA3D8']
    
    @staticmethod
    def create_kpi_card(value, title, delta=None, delta_color="green"):
        """
        Create a KPI card figure.
        
        Args:
            value: Main metric value
            title: KPI title
            delta: Change value (optional)
            delta_color: Color for delta (green/red)
        """
        fig = go.Figure()
        
        # Main value
        fig.add_trace(go.Indicator(
            mode="number+delta" if delta is not None else "number",
            value=value,
            delta={'reference': value - delta if delta else value, 'relative': False} if delta else None,
            title={'text': title, 'font': {'size': 16, 'color': GRAY}},
            number={'font': {'size': 48, 'color': NAVY_BLUE, 'family': 'Arial Black'}},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        return fig
    
    @staticmethod
    def create_line_chart(df, x_col, y_col, title, color=NAVY_BLUE, show_markers=True):
        """
        Create a line chart with brand styling.
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers' if show_markers else 'lines',
            line=dict(color=color, width=3),
            marker=dict(size=8, color=color, symbol='circle'),
            name=y_col
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE, family='Arial')),
            xaxis=dict(
                title=x_col,
                showgrid=True,
                gridcolor=LIGHT_GRAY,
                linecolor=GRAY
            ),
            yaxis=dict(
                title=y_col,
                showgrid=True,
                gridcolor=LIGHT_GRAY,
                linecolor=GRAY
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            height=400,
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(df, x_col, y_col, title, orientation='v', color=NAVY_BLUE):
        """
        Create a bar chart with brand styling.
        """
        if orientation == 'h':
            fig = go.Figure(go.Bar(
                x=df[y_col],
                y=df[x_col],
                orientation='h',
                marker=dict(color=color, line=dict(color=NAVY_BLUE, width=1))
            ))
        else:
            fig = go.Figure(go.Bar(
                x=df[x_col],
                y=df[y_col],
                marker=dict(color=color, line=dict(color=NAVY_BLUE, width=1))
            ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY),
            yaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY),
            height=400,
            margin=dict(l=60, r=40, t=60, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(df, names_col, values_col, title):
        """
        Create a pie chart with brand colors.
        """
        colors = VisualizationHelper.get_color_palette()
        
        fig = go.Figure(go.Pie(
            labels=df[names_col],
            values=df[values_col],
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textposition='auto',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            showlegend=True,
            legend=dict(orientation='v', x=1.1, y=0.5)
        )
        
        return fig
    
    @staticmethod
    def create_stacked_bar_chart(df, x_col, y_cols, title):
        """
        Create a stacked bar chart.
        """
        colors = VisualizationHelper.get_color_palette()
        fig = go.Figure()
        
        for i, col in enumerate(y_cols):
            fig.add_trace(go.Bar(
                x=df[x_col],
                y=df[col],
                name=col,
                marker=dict(color=colors[i % len(colors)])
            ))
        
        fig.update_layout(
            barmode='stack',
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY),
            yaxis=dict(showgrid=True, gridcolor=LIGHT_GRAY),
            height=400,
            margin=dict(l=60, r=40, t=60, b=60),
            legend=dict(orientation='h', y=1.1, x=0.5, xanchor='center')
        )
        
        return fig
    
    @staticmethod
    def create_gauge_chart(value, title, max_value=100, thresholds=[30, 70]):
        """
        Create a gauge chart for metrics like adoption rate.
        """
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': title, 'font': {'size': 18, 'color': NAVY_BLUE}},
            gauge={
                'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': GRAY},
                'bar': {'color': NAVY_BLUE},
                'bgcolor': 'white',
                'borderwidth': 2,
                'bordercolor': GRAY,
                'steps': [
                    {'range': [0, thresholds[0]], 'color': '#FFE5E5'},
                    {'range': [thresholds[0], thresholds[1]], 'color': '#FFF8DC'},
                    {'range': [thresholds[1], max_value], 'color': '#E5F5E5'}
                ],
                'threshold': {
                    'line': {'color': GOLD, 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=40, r=40, t=60, b=40),
            paper_bgcolor='white'
        )
        
        return fig
    
    @staticmethod
    def create_funnel_chart(df, stage_col, value_col, title):
        """
        Create a funnel chart for conversion analysis.
        """
        fig = go.Figure(go.Funnel(
            y=df[stage_col],
            x=df[value_col],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(color=NAVY_BLUE)
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            height=400,
            margin=dict(l=60, r=40, t=60, b=40)
        )
        
        return fig
    
    @staticmethod
    def create_heatmap(df, x_col, y_col, value_col, title):
        """
        Create a heatmap for correlation or intensity visualization.
        """
        pivot_df = df.pivot(index=y_col, columns=x_col, values=value_col)
        
        fig = go.Figure(go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale=[[0, 'white'], [0.5, LIGHT_BLUE], [1, NAVY_BLUE]],
            text=pivot_df.values,
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Value")
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            height=400,
            margin=dict(l=80, r=40, t=60, b=60)
        )
        
        return fig
    
    @staticmethod
    def create_waterfall_chart(categories, values, title):
        """
        Create a waterfall chart for cumulative analysis.
        """
        fig = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=["relative"] * (len(categories) - 1) + ["total"],
            x=categories,
            y=values,
            connector={"line": {"color": GRAY}},
            increasing={"marker": {"color": GOLD}},
            decreasing={"marker": {"color": NAVY_BLUE}},
            totals={"marker": {"color": LIGHT_BLUE}}
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=NAVY_BLUE)),
            height=400,
            margin=dict(l=60, r=40, t=60, b=60),
            showlegend=False
        )
        
        return fig
