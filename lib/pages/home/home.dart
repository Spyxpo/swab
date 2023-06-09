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
      text: 'Overview',
    ),
    SidebarItem(
      icon: CupertinoIcons.paintbrush,
      text: 'Branding',
    ),
    SidebarItem(
      icon: CupertinoIcons.link,
      text: 'Link Handling',
    ),
    SidebarItem(
      icon: CupertinoIcons.square_stack,
      text: 'Interface',
    ),
    SidebarItem(
      icon: CupertinoIcons.globe,
      text: 'Website Overrides',
    ),
    SidebarItem(
      icon: CupertinoIcons.lock,
      text: 'Permissions',
    ),
    SidebarItem(
      icon: CupertinoIcons.location,
      text: 'Native Navigation',
    ),
    SidebarItem(
      icon: CupertinoIcons.plus_app,
      text: 'Plugins',
    ),
    SidebarItem(
      icon: CupertinoIcons.cloud_download,
      text: 'Build & Download',
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
            switchIconCollapsed: CupertinoIcons.chevron_right_circle,
            switchIconExpanded: CupertinoIcons.chevron_left_circle,
            expanded: false,
            items: items,
            selectedIndex: activeTab,
            autoSelectedIndex: false,
            onItemSelected: (index) => setState(() => activeTab = index),
            duration: const Duration(milliseconds: 200),
            minSize: 90,
            maxSize: 230,
            itemIconSize: 18,
            itemIconColor: Colors.white,
            itemHoverColor: Colors.grey.withOpacity(0.3),
            itemSelectedColor: Colors.grey.withOpacity(0.3),
            itemTextStyle: const TextStyle(color: Colors.white, fontSize: 16),
            itemSelectedBorder: const BorderRadius.all(
              Radius.circular(10),
            ),
            itemMargin: 16,
            itemSpaceBetween: 8,
            header: Image.asset(
              'assets/images/logo.png',
              width: 50,
              height: 50,
            ),
            headerText: ' Example',
          ),
          mainScreen(),
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

  Widget mainScreen() {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.only(right: 15.0, top: 18.0, bottom: 18.0),
        child: Container(
          decoration: BoxDecoration(
            color: const Color.fromARGB(166, 57, 57, 57),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: Colors.grey.withOpacity(0.3),
              width: 1,
            ),
          ),
          child: IndexedStack(
            index: activeTab,
            children: [
              Container(),
            ],
          ),
        ),
      ),
    );
  }
}

class NotSupported extends StatelessWidget {
  const NotSupported({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image(
            image: AssetImage('assets/images/not-supported.png'),
            width: 400,
          ),
          SizedBox(height: 20),
          Text(
            'Please use a larger screen',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 24,
            ),
          ),
          SizedBox(height: 5),
          Text(
            'The screen size is too small to display the content',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }
}
