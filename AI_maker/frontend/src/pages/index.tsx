import React from 'react';
import Head from 'next/head';
import { motion } from 'framer-motion';
import { 
  AcademicCapIcon, 
  CodeBracketIcon, 
  ChartBarIcon,
  RocketLaunchIcon,
  UserGroupIcon,
  CogIcon
} from '@heroicons/react/24/outline';

export default function Home() {
  const features = [
    {
      icon: CodeBracketIcon,
      title: '智能代码分析',
      description: '深度分析代码质量，提供详细的改进建议和最佳实践指导。'
    },
    {
      icon: AcademicCapIcon,
      title: '个性化学习路径',
      description: '根据您的水平和目标，制定专属的学习计划和进度跟踪。'
    },
    {
      icon: ChartBarIcon,
      title: '学习进度跟踪',
      description: '实时监控学习进度，提供数据可视化的学习报告。'
    },
    {
      icon: RocketLaunchIcon,
      title: '项目实战指导',
      description: '引导您完成实际项目开发，从理论到实践的完整学习体验。'
    },
    {
      icon: UserGroupIcon,
      title: '社区互动',
      description: '与其他学习者交流经验，分享代码，共同进步。'
    },
    {
      icon: CogIcon,
      title: '智能推荐',
      description: '基于AI算法，推荐最适合您的学习内容和练习题目。'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>CodeMentor AI - 智能编程导师</title>
        <meta name="description" content="基于AI的个性化编程学习平台" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* 导航栏 */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <CodeBracketIcon className="h-8 w-8 text-indigo-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">CodeMentor AI</span>
            </div>
            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-gray-900">登录</button>
              <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
                开始学习
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 主要内容 */}
      <main>
        {/* Hero 区域 */}
        <section className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-4xl sm:text-6xl font-bold text-gray-900 mb-6">
                智能编程导师
                <span className="text-indigo-600"> CodeMentor AI</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                基于人工智能的个性化编程学习平台，为您提供智能化的代码分析、
                个性化学习路径和实时编程指导，让编程学习更高效、更有趣。
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors">
                  立即开始
                </button>
                <button className="border border-indigo-600 text-indigo-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-50 transition-colors">
                  了解更多
                </button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* 功能特性 */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                强大的学习功能
              </h2>
              <p className="text-xl text-gray-600">
                全方位的编程学习支持，助您快速提升编程技能
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-gray-50 p-6 rounded-lg hover:shadow-lg transition-shadow"
                >
                  <feature.icon className="h-12 w-12 text-indigo-600 mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* 统计数据 */}
        <section className="py-20 bg-indigo-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
              <div>
                <div className="text-4xl font-bold text-white mb-2">10,000+</div>
                <div className="text-indigo-200">活跃学习者</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-white mb-2">50,000+</div>
                <div className="text-indigo-200">代码分析</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-white mb-2">95%</div>
                <div className="text-indigo-200">用户满意度</div>
              </div>
              <div>
                <div className="text-4xl font-bold text-white mb-2">24/7</div>
                <div className="text-indigo-200">AI在线指导</div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA 区域 */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              开始您的编程学习之旅
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              加入我们，体验AI驱动的个性化编程学习
            </p>
            <button className="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-indigo-700 transition-colors">
              免费注册
            </button>
          </div>
        </section>
      </main>

      {/* 页脚 */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">CodeMentor AI</h3>
              <p className="text-gray-400">
                智能编程导师，让编程学习更简单、更高效。
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">产品</h4>
              <ul className="space-y-2 text-gray-400">
                <li>代码分析</li>
                <li>学习路径</li>
                <li>项目指导</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">支持</h4>
              <ul className="space-y-2 text-gray-400">
                <li>帮助中心</li>
                <li>联系我们</li>
                <li>常见问题</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">社区</h4>
              <ul className="space-y-2 text-gray-400">
                <li>开发者论坛</li>
                <li>代码分享</li>
                <li>学习小组</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 CodeMentor AI. 保留所有权利。</p>
          </div>
        </div>
      </footer>
    </div>
  );
} 