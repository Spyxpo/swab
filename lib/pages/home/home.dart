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

  late TextEditingController appNameController = TextEditingController();
  late TextEditingController appPackageController = TextEditingController();
  late TextEditingController urlController = TextEditingController();
  late TextEditingController appDescriptionController = TextEditingController();
  late TextEditingController contactEmailController = TextEditingController();
  late TextEditingController privacyPolicyController = TextEditingController();
  late TextEditingController termsAndConditionController =
      TextEditingController();

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
    setState(() {
      urlController = TextEditingController(text: "https://");
    });
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
            child: const SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.only(left: 15.0, right: 15.0),
                child: Simulator(url: 'https://www.spyxpo.com'),
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
              Center(
                child: ScrollConfiguration(
                  behavior: ScrollConfiguration.of(context)
                      .copyWith(scrollbars: false),
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        const SizedBox(height: 10),
                        const Text(
                          'Overview',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 10),
                        const Text(
                          'Configure your app\'s basic settings',
                          style: TextStyle(
                            color: Colors.grey,
                            fontSize: 16,
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'App Name',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.app_badge,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appNameController,
                            placeholder: 'Enter App Name',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'App Package Name',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.cube_box,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appPackageController,
                            placeholder: 'com.example.app',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'Website URL',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.link,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: urlController,
                            placeholder: 'https://www.example.com',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            onSubmitted: (value) {
                              setState(() {
                                urlController.text = value;
                              });
                            },
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'App Description',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding:
                                  EdgeInsets.only(left: 10.0, bottom: 23.0),
                              child: Icon(
                                CupertinoIcons.text_bubble,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: appDescriptionController,
                            placeholder: 'Enter App Description',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            maxLines: 2,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'Contact Email',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.mail,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            controller: contactEmailController,
                            placeholder: 'contact@example.com',
                            keyboardType: TextInputType.emailAddress,
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'Privacy Policy URL',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.doc,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: privacyPolicyController,
                            placeholder: 'Privacy Policy URL',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        const Text(
                          'Terms & Conditions URL',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 5),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoTextField(
                            padding: const EdgeInsets.all(10),
                            prefix: const Padding(
                              padding: EdgeInsets.only(left: 10.0),
                              child: Icon(
                                CupertinoIcons.doc,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            decoration: BoxDecoration(
                              color: Colors.grey.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(10),
                            ),
                            controller: termsAndConditionController,
                            placeholder: 'Terms & Conditions URL',
                            placeholderStyle: const TextStyle(
                              color: Colors.grey,
                              fontSize: 16,
                            ),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),
                        SizedBox(
                          width: MediaQuery.of(context).size.width * 0.3,
                          child: CupertinoButton(
                            padding: const EdgeInsets.all(10),
                            color: Colors.blue,
                            borderRadius: BorderRadius.circular(10),
                            onPressed: () {
                              setState(() {});
                            },
                            child: const Text(
                              'Next',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
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
