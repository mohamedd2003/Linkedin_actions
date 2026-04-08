import os
import requests
from datetime import datetime, timedelta

class SearchEngine:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY', '').strip().strip('"').strip("'")
        if not self.api_key:
            raise ValueError("SERPER_API_KEY not found in environment variables")
        
        self.base_url = "https://google.serper.dev/search"
    
    def search_ai_topics(self):
        """البحث عن أحدث مواضيع AI و NLP و LLMs"""
        
 queries = [
    "Next.js 16 latest features and App Router updates",
    "Advanced React Server Components (RSC) and Streaming patterns",
    "Frontend Performance Optimization and Core Web Vitals (INP/LCP)",
    "TypeScript 5.x Best Practices for Scalable Web Applications",
    "Modern State Management: Zustand vs React Query vs Context API",
    "Micro-Frontends Architecture and Module Federation in 2026",
    "Optimizing Bundle Size with Tree Shaking and Turbopack",
    "Headless UI Libraries and Accessible Design Systems (Radix, Headless UI)",
    "Edge Runtime and Middleware Patterns in Next.js",
    "Partial Prerendering (PPR) and Static vs Dynamic Rendering",
    "React 19 Actions and the new 'use' hook implementation",
    "Server-side Form Validation in Next.js with Zod",
    "Next-intl for Localization and RTL Support in Arabic Web Apps",
    "Advanced Tailwind CSS patterns and Container Queries",
    "Testing React Components with Vitest and Playwright",
    "Client-side Caching Strategies and Service Workers (PWA)",
    "Hydration Error Debugging in Next.js and React",
    "CSS-in-JS vs Zero-runtime CSS (Vanilla Extract, Panda CSS)",
    "Optimizing Web Fonts and Image Optimization with Next/Image",
    "Integrating AI SDKs in React for Generative UI",
    "WebAssembly (WASM) use cases for high-performance Frontend",
    "The transition from Webpack to Vite and Rsbuild",
    "Shadcn/ui customization and component governance",
    "React Native vs Expo for Web: Cross-platform code sharing",
    "Deep dive into JavaScript Event Loop and V8 Engine optimization",
    "Monorepo management with TurboRepo and Nx for Frontend",
    "Browser Security Best Practices: CSP, XSS, and CSRF protection",
    "Inter-component communication patterns without Prop Drilling",
    "Optimistic UI updates with useOptimistic hook",
    "Handling Arithmetic Overflow and High-Performance Data Rendering in JS"
]
        all_results = []
        
        for query in queries:
            try:
                response = requests.post(
                    self.base_url,
                    headers={
                        'X-API-KEY': self.api_key,
                        'Content-Type': 'application/json'
                    },
                    json={
                        'q': query,
                        'num': 5,
                        'gl': 'us',
                        'hl': 'en'
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'organic' in data:
                        for result in data['organic']:
                            all_results.append({
                                'title': result.get('title', ''),
                                'snippet': result.get('snippet', ''),
                                'link': result.get('link', ''),
                                'source': result.get('source', '')
                            })
            
            except Exception as e:
                print(f"Error searching for {query}: {e}")
                continue
        
        return all_results
    
    def filter_quality_sources(self, results):
        """تصفية المصادر الموثوقة فقط"""
        
       trusted_domains = [
    // Official Docs & Frameworks
    'nextjs.org',
    'react.dev',
    'vercel.com',
    'typescriptlang.org',
    'tailwindcss.com',
    'nodejs.org',
    
    // Technical Reference & Standard
    'developer.mozilla.org',
    'web.dev',
    'javascript.info',
    
    // Community & News
    'github.com',
    'stackoverflow.com',
    'dev.to',
    'hashnode.com',
    'medium.com/engineering',
    'tldr.tech', // من أقوى النشرات الإخبارية للمبرمجين
    
    // Engineering Blogs (التقيلة)
    'engineering.fb.com', // Meta Engineering
    'netflixtechblog.com',
    'github.blog/category/engineering',
    'stripe.com/blog/engineering',
    'discord.com/category/engineering',
    'cloudinary.com/blog', // مهم جداً للـ Image/Video optimization
    
    // X (Twitter) High-Value Handles (Domains to watch)
    'x.com/dan_abramov', // الأب الروحي لـ React
    'x.com/leeerob', // Lee Robinson (Next.js/Vercel)
    'x.com/t3dotgg', // Theo - شخصية مؤثرة في الـ T3 Stack
    'x.com/addyosmani', // Google Chrome Engineer
    'x.com/kentcdodds', // Remix & Testing expert
    'x.com/shadcn', // creator of shadcn/ui
    
    // Tooling & Performance
    'tanstack.com',
    'bundlephobia.com',
    'sentry.io/answers', // مفيد جداً في حل الـ Errors المشهورة
    'builder.io/blog' // مركزين جداً على الـ Visual Dev والـ Performance
]
        
        filtered = []
        
        for result in results:
            link = result.get('link', '').lower()
            
            # التحقق من المصدر الموثوق
            is_trusted = any(domain in link for domain in trusted_domains)
            
            # التحقق من وجود محتوى تقني
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            tech_keywords = ['ai', 'model', 'llm', 'nlp', 'machine learning', 
                           'neural', 'research', 'algorithm', 'data', 'training']
            
            has_tech_content = any(keyword in title or keyword in snippet 
                                  for keyword in tech_keywords)
            
            if is_trusted and has_tech_content:
                filtered.append(result)
        
        return filtered
    
    def get_best_topic(self):
        """البحث واختيار أفضل موضوع"""
        
        results = self.search_ai_topics()
        
        if not results:
            return None
        
        filtered = self.filter_quality_sources(results)
        
        if not filtered:
            return results[0] if results else None
        
        return filtered[0]
