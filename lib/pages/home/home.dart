import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:swab/pages/pages.dart';
import 'package:swab/widgets/widgets.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  int activeTab = 0;
  late TextEditingController urlController = TextEditingController();

  final List<SidebarItem> items = [
    SidebarItem(
      icon: CupertinoIcons.home,
      text: 'Home',
    ),
    SidebarItem(
      icon: CupertinoIcons.bell,
      text: 'Notifications',
    ),
    SidebarItem(
      icon: CupertinoIcons.alarm,
      text: 'Integrations',
    ),
    SidebarItem(
      icon: CupertinoIcons.settings,
      text: 'Settings',
    ),
  ];

  @override
  void initState() {
    super.initState();
    urlController = TextEditingController();
  }

  @override
  void dispose() {
    urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          AnimatedSidebar(
            switchIconCollapsed: CupertinoIcons.chevron_right_square,
            switchIconExpanded: CupertinoIcons.chevron_left_square,
            expanded: MediaQuery.of(context).size.width > 600,
            items: items,
            selectedIndex: activeTab,
            autoSelectedIndex: false,
            onItemSelected: (index) => setState(() => activeTab = index),
            duration: const Duration(milliseconds: 200),
            minSize: 90,
            maxSize: 250,
            itemIconSize: 18,
            itemIconColor: Colors.white,
            itemHoverColor: Colors.grey.withOpacity(0.3),
            itemSelectedColor: Colors.grey.withOpacity(0.3),
            itemTextStyle: const TextStyle(color: Colors.white, fontSize: 16),
            itemSelectedBorder: const BorderRadius.all(
              Radius.circular(5),
            ),
            itemMargin: 16,
            itemSpaceBetween: 5,
            header: Image.asset(
              'assets/images/logo.png',
              width: 50,
              height: 50,
            ),
            headerText: ' Example',
          ),
          SizedBox(
            width: 120,
            child: CupertinoTextField(
              controller: urlController,
              onSubmitted: (value) {
                setState(() {
                  urlController.clear();
                  urlController.text = value;
                });
              },
            ),
          ),
          Container(
            decoration: BoxDecoration(
              border: Border.all(
                color: Colors.grey.withOpacity(0.3),
                width: 1,
              ),
            ),
            child: SingleChildScrollView(
              child: Padding(
                padding: const EdgeInsets.only(left: 15.0, right: 15.0),
                child: Simulator(url: urlController.text),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildPage(int idx) {
    return Wrap(
      children: [],
    );
  }
}
