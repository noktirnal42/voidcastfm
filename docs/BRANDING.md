# VoidCastFM Brand Guidelines

## Brand Identity

**VoidCastFM** represents the intersection of professional radio technology and modern design aesthetics. Our brand embodies precision, innovation, and accessibility in the amateur radio community.

## Logo

### Concept
The VoidCastFM logo visualizes radio frequency waves emerging from emptiness - representing the transmission of signals from the void into reality. The design combines:
- Radio wave patterns (sine waves)
- Void/empty space (negative space)
- Modern, minimalist aesthetics

### Usage
- Always maintain clear space around the logo
- Minimum size: 24px height for digital use
- Use approved color variations only

## Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Void Cyan** | `#00f5ff` | `rgb(0, 245, 255)` | Primary accent, buttons, highlights |
| **Electric Purple** | `#8b5cf6` | `rgb(139, 92, 246)` | Secondary accent, gradients |
| **Deep Space** | `#08080f` | `rgb(8, 8, 15)` | Background, dark surfaces |
| **Alert Red** | `#ff3c3c` | `rgb(255, 60, 60)` | Warnings, stop actions, errors |

### Secondary Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Warm Yellow** | `#f5c842` | Warnings, temperature indicators |
| **Orange** | `#ff8c00` | Medium alerts, heat |
| **Neon Pink** | `#ff0080` | Live indicators, streaming |
| **Lavender** | `#c4b5fd` | Secondary text, subtle highlights |

### Gradients

**Primary Gradient:**
```css
linear-gradient(135deg, #00f5ff, #8b5cf6)
```

**Alert Gradient:**
```css
linear-gradient(135deg, #ff3c3c, #ff0080)
```

**Void Background:**
```css
linear-gradient(180deg, #08080f 0%, #0a0a12 100%)
```

## Typography

### Primary Font
**SF Mono** (Apple System Monospace)
- Used for all UI text, code, and technical content
- System default on macOS

### Fallback Fonts
1. JetBrains Mono
2. Fira Code
3. Monaco
4. Consolas

### Font Sizes
- **Headlines**: 22px - 28px
- **Body**: 14px - 16px
- **Small/Captions**: 10px - 12px
- **Micro**: 9px

### Font Weights
- **Regular**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

## Voice & Tone

### Personality
- **Professional** but approachable
- **Technical** but accessible
- **Precise** without being cold
- **Innovative** yet reliable

### Writing Guidelines
- Use clear, concise language
- Avoid unnecessary jargon
- Explain technical terms when first used
- Maintain an encouraging tone for beginners
- Respect the expertise of experienced users

### Examples

**✅ Good:**
> "Transform your Raspberry Pi into a professional-grade RF transmitter with complete macOS control."

**❌ Avoid:**
> "Leverage our synergistic RF solution paradigm for optimal transmission outcomes."

## UI Design Principles

### 1. Dark-First Design
All interfaces optimized for dark environments and extended use sessions.

### 2. Glassmorphism
Use backdrop blur and transparency for depth:
```css
backdrop-filter: blur(24px) saturate(150%);
background: rgba(12, 12, 20, 0.7);
border: 1px solid rgba(0, 245, 255, 0.1);
```

### 3. Neon Accents
Glowing effects for interactive elements:
```css
box-shadow: 0 0 16px rgba(0, 245, 255, 0.2);
```

### 4. Mesh Gradients
Subtle animated backgrounds:
```css
background: 
  radial-gradient(ellipse at 15% 20%, rgba(0, 245, 255, 0.06) 0%, transparent 50%),
  radial-gradient(ellipse at 85% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 50%);
```

## Iconography

### Style
- Minimalist, line-based icons
- Consistent stroke width (2px)
- Rounded corners where appropriate
- Clear visual metaphors

### Common Icons
- 📡 Transmission/Radio
- ⚡ Power/Active
- 🔗 Connection/Link
- ⚙️ Settings/Configuration
- 🎤 Audio/Microphone
- 📊 Spectrum/Analysis
- 🚨 Alert/Emergency

## Application Examples

### App Icon
- Circular or rounded square base
- Radio wave motif
- Void Cyan on Deep Space background
- Minimal text (optional "VF" or wave symbol)

### Splash Screen
- Deep Space background
- Animated mesh gradient
- VoidCastFM wordmark
- Version information

### Documentation
- Clean, readable layout
- VoidCastFM header with logo
- Cyan accent colors for links
- Consistent heading hierarchy

## Social Media

### Profile Images
- Square format
- Logo centered on Deep Space background
- Minimum padding: 20%

### Post Templates
- Dark background with mesh gradient
- Void Cyan headlines
- White or light gray body text
- Electric Purple accents

## Merchandise (Future)

### T-Shirts
- Deep Space or black base
- Void Cyan or Electric Purple print
- Minimalist wave logo

### Stickers
- Die-cut logo shape
- Holographic or matte finish
- Various sizes (2", 3", 4")

## Contact

For brand-related questions or to report misuse:
- Email: [Your contact]
- GitHub Discussions: [Link]

---

**Version:** 1.0.0  
**Last Updated:** April 2026  
**Maintained By:** VoidCastFM Team
