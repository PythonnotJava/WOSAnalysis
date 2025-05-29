# def complete_task2(app):
#     filePath = open_file(app)
#     if not filePath:
#         QMessageBox.warning(
#             app,
#             '警告',
#             '您取消了选择文件',
#             QMessageBox.StandardButton.Ok
#         )
#     else:
#         # 先清屏
#         app.tabs.recover()
#         for i in range(app.tabs.count() - 1):
#             app.tabs.removeTab(1)
#         # 继续
#         data_so, data_py = journal_statistics(load(filePath))
#         states = get_state(app)
#         state_so, state_py = states['so'], states['py']
#         so1, py1 = None, None
#         # so系列
#         if state_so['checked']:
#             len_so = len(data_so)
#             so1 = len_so
#             spin_so = min(state_so['spin'], len_so)
#             spin_so = len_so if spin_so == 0 else spin_so
#             if state_so['select'] == '从小到大':
#                 data_so = sort_value(data_so, reverse=False)
#             elif state_so['select'] == '从大到小':
#                 data_so = sort_value(data_so, reverse=True)
#             else:
#                 pass
#             data_slice_so = SliceableDict(data_so)[:spin_so]
#             # 输出Json
#             if state_so['json']:
#                 app.tabs.addTab(JsonPage(data_slice_so), qtIcon('mdi.code-json'), 'Json格式')
#             # 画纵向柱状图
#             if state_so['bar']:
#                 app.tabs.addTab(MpWdiegt(draw_bar(
#                     data_slice_so,
#                     title=state_so['title'],
#                     horizontal=False
#                 )), qtIcon('fa5s.chart-bar'), 'Bar')
#             # 画横向柱状图
#             if state_so['barh']:
#                 app.tabs.addTab(MpWdiegt(draw_bar(
#                     data_slice_so,
#                     title=state_so['title'],
#                     horizontal=True
#                 )), qtIcon('fa6.chart-bar'), 'Barh')
#             # 画云图
#             if state_so['cloud']:
#                 app.tabs.addTab(MpWdiegt(draw_word_cloud(
#                     data_slice_so,
#                     title=state_so['title'],
#                 )), qtIcon('ei.cloud'), '词云图')
#         # py系列
#         if state_py['checked']:
#             len_py = len(data_py)
#             py1 = len_py
#             spin_py = min(state_py['spin'], len_py)
#             spin_py = len_py if spin_py == 0 else spin_py
#             if state_py['select'] == '从早到晚':
#                 data_py = sort_key(data_py, reverse=False)
#             elif state_py['select'] == '从晚到早':
#                 data_py = sort_key(data_py, reverse=True)
#             else:
#                 pass
#             data_slice_py = SliceableDict(data_py)[:spin_py]
#             # 输出Json
#             if state_py['json']:
#                 app.tabs.addTab(JsonPage(data_slice_py), qtIcon('mdi.code-json'), 'Json格式')
#             # 画纵向柱状图
#             if state_py['bar']:
#                 app.tabs.addTab(MpWdiegt(draw_bar(
#                     data_slice_py,
#                     title=state_py['title'],
#                     horizontal=False
#                 )), qtIcon('fa5s.chart-bar'), 'Bar')
#             # 画横向柱状图
#             if state_py['barh']:
#                 app.tabs.addTab(MpWdiegt(draw_bar(
#                     data_slice_py,
#                     title=state_py['title'],
#                     horizontal=True
#                 )), qtIcon('fa6.chart-bar'), 'Barh')
#             # 画云图
#             if state_py['cloud']:
#                 app.tabs.addTab(MpWdiegt(draw_word_cloud(
#                     data_slice_py,
#                     title=state_py['title'],
#                 )), qtIcon('ei.cloud'), '词云图')
#         app.tabs.refresh(py1, so1)
#         QMessageBox.information(
#             app,
#             '通知',
#             '导入成功',
#             QMessageBox.StandardButton.Ok
#         )
#
